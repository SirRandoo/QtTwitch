# This file is part of QtTwitch.
#
# QtTwitch is free software:
# you can redistribute it
# and/or modify it under the
# terms of the GNU Lesser General
# Public License as published by
# the Free Software Foundation,
# either version 3 of the License,
# or (at your option) any later
# version.
#
# QtTwitch is distributed in
# the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without
# even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more
# details.
#
# You should have received a copy of the
# GNU Lesser General Public License along
# with QtTwitch.  If not,
# see <https://www.gnu.org/licenses/>.
import datetime
import functools
import logging
import random
import re
import typing

from PyQt5 import QtCore, QtWebSockets

from QtUtilities import signals
from ..data.irc import PrivateMessage

logger = logging.getLogger(__name__)

__all__ = {"Gateway"}


class Gateway(QtCore.QObject):
    """A class for interacting with Twitch's IRC servers."""

    # Signals
    on_priv_limit_reset = QtCore.pyqtSignal()
    on_join_limit_reset = QtCore.pyqtSignal()
    on_whisper_second_reset = QtCore.pyqtSignal()
    on_whisper_minute_reset = QtCore.pyqtSignal()
    on_whisper_account_reset = QtCore.pyqtSignal()

    on_message = QtCore.pyqtSignal(str)
    on_user_join = QtCore.pyqtSignal(str, str)  # Channel, user login
    on_user_part = QtCore.pyqtSignal(str, str)  # Channel, user login
    on_user_modded = QtCore.pyqtSignal(str, str)  # Channel, user login
    on_user_unmodded = QtCore.pyqtSignal(str, str)  # Channel, user login
    on_names_received = QtCore.pyqtSignal(str, list)  # Channel, names list (partial)
    on_user_banned = QtCore.pyqtSignal(str, str, int)  # Channel, reason, duration
    on_global_user_state = QtCore.pyqtSignal(object)  # QState
    
    on_chat_cleared = QtCore.pyqtSignal()
    on_user_chat_cleared = QtCore.pyqtSignal(str, str)  # Channel, user login
    on_channel_hosting = QtCore.pyqtSignal(str, str)  # Channel, hosted channel
    on_channel_unhosted = QtCore.pyqtSignal(str)  # Channel
    
    def __init__(self, **kwargs):
        """
        :param parent: The parent QObject for this connection.
        :param channel: The channel to connect to upon login.
        :param channels: A list of channels to connect to upon login.
        :param nick: The name to use during the login process.
        :param token: The OAuth token to use during the login process.
        :param host: The host server to connect to.
        :param port: The port to connect to.
        :param whisper_reset: The moment the account limit gets reset.
        """
        # Super Call #
        super(Gateway, self).__init__(parent=kwargs.get('parent'))
        
        # "Public" Attributes #
        self.channels: typing.List[str] = []
        self.whisper_reset: datetime.datetime = kwargs.get('whisper_reset', None)
        
        # "Private" Attributes #
        self._nick: str = kwargs.get('nick', 'justinfan2389')
        self._token: str = kwargs.get('token', 'foobar')
        self._host: str = kwargs.get('host', 'irc-ws.chat.twitch.tv')
        self._port: int = kwargs.get('port', 443)
        
        # "Internal" Attributes #
        self._socket = QtWebSockets.QWebSocket(parent=self)
        self._timer = QtCore.QTimer(parent=self)
        
        self._whisper_second_started: bool = False
        self._whisper_minute_started: bool = False
        self._whisper_daily_started: bool = False
        self._join_started: bool = False
        self._priv_started: bool = False
        self._should_reconnect: bool = True
        
        self._reset_join_limit_auto = functools.partial(self.reset_join_limit, automated=True)
        self._reset_priv_limit_auto = functools.partial(self.reset_priv_limit, automated=True)
        self._reset_w_second_auto = functools.partial(self.reset_whisper_seconds, automated=True)
        self._reset_w_minute_auto = functools.partial(self.reset_whisper_minutes, automated=True)
        self._reset_w_daily_auto = functools.partial(self.reset_whisper_daily, automated=True)
        
        # Ratelimiting Attributes
        self._priv_sent: int = 0
        self._priv_limit: int = 20
        self._priv_period: int = 30  # Seconds
        
        self._join_sent: int = 0
        self._join_limit: int = 50
        self._join_period: int = 15  # Seconds
        
        self._whispers_this_second: int = 0  # Whispers sent this second
        self._whispers_this_minute: int = 0  # Whispers sent this minute
        self._whispered_accounts: typing.List[str] = []  # The accounts whispered.
        
        self._whisper_second_limit: int = 3
        self._whisper_minute_limit: int = 200  # Messages per minute
        self._whisper_accounts_limit: int = 40
        
        self._reconnect_attempts: int = 0
        
        self._priv_regex = re.compile(r'@(?P<tags>.*) :(?P<name>\w+)!(?P=name)@(?P=name)\.\w\.w\.\w+ PRIVMSG '
                                      r'#(?P<channel>\w+]) :(?P<message>.*)')
        
        # "Internal" Calls #
        self._socket.error.connect(self.process_errors)
        self._socket.connected.connect(self.process_connection)
        self._socket.disconnected.connect(self.process_disconnection)
        self._socket.textMessageReceived.connect(self.process_message)

        self.qt_disconnect = super(Gateway, self).disconnect
        
        # Validation #
        if self._token != "foobar" and not self._token.startswith("oauth"):
            self._token = f'oauth:{self._token}'
    
    # Utility Methods #
    def ban(self, channel: str, user: str, reason: str = None):
        """Bans `user` in `channel` for `reason`."""
        if reason is None:
            reason = ''
        
        self.send_priv_message(channel, f'.ban {user} {reason}')
    
    def unban(self, channel: str, user: str):
        """Unbans `user` from `channel`."""
        self.send_priv_message(channel, f'.unban {user}')
    
    def timeout(self, channel: str, user: str, duration: int = None, reason: str = None):
        """Times out `user` in `channel` for `duration` seconds with `reason`."""
        if duration is None:
            duration = 600  # 10 minutes
        
        if reason is None:
            reason = ''
        
        self.send_priv_message(channel, f'.timeout {user} {duration} {reason}')
    
    def color(self, color: str, channel: str = None):
        """Changes the color of the account's username to `color`."""
        if channel is None:
            channel = self.channels[random.randint(len(self.channels) - 1)]
        
        self.send_priv_message(channel, f'.color {color}')
    
    def me(self, channel: str, text: str):
        """Sends a colored message."""
        self.send_priv_message(channel, f'.me {text}')
    
    def join(self, channel: str):
        """Joins a channel on Twitch."""
        self.send_raw_message(f'JOIN #{channel}')

        if channel not in self.channels:
            self.channels.append(channel)
    
    def part(self, channel: str):
        """Leaves a channel."""
        self.send_raw_message(f'PART #{channel}')

        if channel in self.channels:
            self.channels.remove(channel)
    
    def slow(self, channel: str, limit: int = None):
        """Enables slow mode in `channel` with a limit of `limit` seconds."""
        if limit is None:
            limit = 120
        
        self.send_priv_message(channel, f'.slow {limit}')
    
    def slowoff(self, channel: str):
        """Disables slow mode for `channel`."""
        self.send_priv_message(channel, '.slowoff')
    
    def followers(self, channel: str, *, mins: int = None, hrs: int = None, days: int = None, wks: int = None,
                  mnths: int = None):
        """Enables follower only mode in `channel` for duration."""
        duration = 0
        
        if mnths:
            duration = f'{mnths}mo'
        
        if wks:
            duration += f'{wks}mo'
        
        if days:
            duration += f'{days}d'
        
        if hrs:
            duration += f'{hrs}h'
        
        if mins:
            duration += f'{mins}m'
        
        self.send_priv_message(channel, f'.followers {duration}')
    
    def followersoff(self, channel: str):
        """Disables follower only mode for `channel`."""
        self.send_priv_message(channel, '.followersoff')
    
    def subscribers(self, channel: str):
        """Enables subscriber only mode for `channel`."""
        self.send_priv_message(channel, '.subscribers')
    
    def subscribersoff(self, channel: str):
        """Disables subscriber only mode for `channel`."""
        self.send_priv_message(channel, '.subscribersoff')
    
    def clear(self, channel: str):
        """Clears the chat in `channel`."""
        self.send_priv_message(channel, '.clear')
    
    def r9kbeta(self, channel: str):
        """Enables R9KBeta in `channel`."""
        self.send_priv_message(channel, '.r9kbeta')
    
    def r9kbetaoff(self, channel: str):
        """Disables R9KBeta in `channel`."""
        self.send_priv_message(channel, '.r9kbetaoff')
    
    def emoteonly(self, channel: str):
        """Enables emote only mode in `channel`."""
        self.send_priv_message(channel, '.emoteonly')
    
    def emoteonlyoff(self, channel: str):
        """Disables emote only mode in `channel`."""
        self.send_priv_message(channel, '.emoteonlyoff')
    
    def mod(self, channel: str, user: str):
        """Promotes `user` to a moderator in `channel`."""
        self.send_priv_message(channel, f'.mod {user}')
    
    def unmod(self, channel: str, user: str):
        """Demote `user` to a viewer in `channel`."""
        self.send_priv_message(channel, f'.unmod {user}')
    
    def host(self, channel: str, target: str):  # This might not work
        """Sets `channel` into host mode for `target`."""
        self.send_priv_message(channel, f'.host {target}')
    
    def unhost(self, channel: str):  # This might not work
        """Disables host mode for `channel`."""
        self.send_priv_message(channel, '.unhost')
    
    def vip(self, channel: str, user: str):
        """Promotes `user` to a VIP in `channel`"""
        self.send_priv_message(channel, f'.vip {user}')
    
    def unvip(self, channel: str, user: str):
        """Demotes `user` to a viewer in `channel`."""
        self.send_priv_message(channel, f'.unvip {user}')
    
    def delete(self, channel: str, message_id: str):
        """Deletes message with `message_id` in `channel`."""
        self.send_priv_message(channel, f'.delete {message_id}')
    
    # Connection Methods #
    def connect(self, *, host: str = None, port: int = None):
        """Connects to the specified host on the specified port.  If no
        connection details were provided during the creation of this class,
        `host` and `port` must be specified."""
        # Validation
        if not self._host and host is None:
            raise ConnectionAbortedError("No host specified!")
        
        elif host is not None:
            self._host = host
        
        if not self._port and port is None:
            raise ConnectionAbortedError("No port specified!")
        
        elif port is not None:
            self._port = port
        
        # Connection logic
        self._socket.open(QtCore.QUrl(f'wss://{self._host}:{self._port}/'))
    
    def process_connection(self):
        """Continues connecting to Twitch's IRC server."""
        if self._socket.isValid():
            if not self._join_started:
                self._timer.singleShot(self._join_period * 1000, self._reset_join_limit_auto)
                self._join_started = True
            
            # Send credentials
            self.send_raw_message(f'PASS {self._token}')
            self.send_raw_message(f'NICK {self._nick}')
            
            # Request capabilities
            self.send_raw_message("CAP REQ :twitch.tv/membership")
            self.send_raw_message("CAP REQ :twitch.tv/tags")
            self.send_raw_message("CAP REQ :twitch.tv/commands")
            
            # Join channels
            for channel in self.channels:
                self.join(channel)
        
        else:
            logger.warning("Could not connect to Twitch's IRC servers!")
            logger.warning(f'Code {self._socket.error()} : {self._socket.errorString()}')
    
    def process_disconnection(self):
        """Processes a disconnection from Twitch's servers."""
        if self._should_reconnect:
            while not self._socket.isValid() or self._reconnect_attempts >= 5:
                self._socket.open(QtCore.QUrl(f'wss://{self._host}:{self._port}/'))
                signals.wait_for_signal(self._socket.connected, timeout=max(self._reconnect_attempts * 5, 1))
                
                self._reconnect_attempts += 1

    def process_errors(self, error: int):
        """Processes any errors the gateway may have."""
    
    # Message Methods #
    def send_raw_message(self, content: str, *, ignore_limit: bool = None):
        """Sends a raw IRC message to Twitch."""
        if ignore_limit is None:
            ignore_limit = False
        
        if not ignore_limit:
            if content.lower().startswith("CAP REQ"):
                self.wait_and_increment_priv()
            
            else:
                self.wait_and_increment_join()
        
        if not content.endswith('\r\n'):
            content += '\r\n'

        self._socket.sendTextMessage(content)
    
    def send_priv_message(self, channel: str, content: str):
        """Sends a PRIVMSG to Twitch's IRC servers."""
        if not self._priv_started:
            self._timer.singleShot(1000 * self._priv_limit, self._reset_priv_limit_auto)
            self._priv_started = True
        
        self.wait_and_increment_priv()
        self.send_raw_message(f'PRIVMSG #{channel} :{content}', ignore_limit=True)
    
    def send_whisper_message(self, user: str, content: str):
        """Sends a whisper message to `user` containing `content`."""
        if not self.can_whisper(user):
            self.wait_for_whisper()
        
        self.send_raw_message(f'PRIVMSG #jtv :.w {user} {content}')
        self.increment_whisper(user)
    
    def process_message(self, message: typing.Union[str, PrivateMessage]):
        """Processes a message presumably from Twitch."""
        if isinstance(message, str):
            user_meta = f'{self._nick}!{self._nick}@{self._nick}.tmi.twitch.tv'
            self.on_message.emit(message)
            
            # Since we're not entirely sure how we want to go about parsing IRC
            # messages, we'll just do it this way.  Eventually we'll want to
            # move to dataclasses.
            # TODO: Recode this to use dataclasses.
            
            if message == 'PING :tmi.twitch.tv\r\n':
                self.send_raw_message('PONG :tmi.twitch.tv', ignore_limit=True)
            
            elif message.startswith(f':{user_meta} JOIN'):
                channel = message[len(f':{user_meta} JOIN #'):].strip()
                
                if channel not in self.channels:
                    self.channels.append(channel)
            
            elif message.startswith(f':{user_meta} PART'):
                channel = message[len(f'{user_meta} PART #'):].strip()
                
                if channel in self.channels:
                    self.channels.remove(channel)
            
            elif message.startswith(':jtv MODE'):
                *_, channel, status, user = message.split(' ')
                
                if status == '+o':
                    self.on_user_modded.emit(channel, user)
                
                elif status == '-o':
                    self.on_user_unmodded.emit(channel, user)
            
            elif message.startswith(':tmi.twitch.tv CLEARCHAT'):
                partial = message.replace(':tmi.twitch.tv CLEARCHAT #', '')
                segments = partial.split(' :')
                
                if len(segments) > 1:
                    channel, user = segments
                    
                    self.on_user_chat_cleared.emit(channel, user)
                
                else:
                    channel = segments
                    
                    self.on_chat_cleared.emit(channel)
            
            else:
                try:
                    self.process_message(PrivateMessage.from_message(None, message))
                
                except ValueError:
                    pass
        
        elif isinstance(message, PrivateMessage):
            logger.warning("Received PrivateMessage instance; this shouldn't have happened!")
            self.process_message(message)

        else:
            raise ValueError(f'Cannot process message type {message.__class__.__name__}!')
    
    # Ratelimit Methods #
    # It's best not to call these methods directly
    def wait_and_increment_priv(self):
        """A utility method for waiting for the PRIVMSG limit to reset, and
        incrementing the counter.  If the counter is within the limit, the
        method will just increment the counter."""
        if self._priv_sent >= self._priv_limit:
            signals.wait_for_signal(self.on_priv_limit_reset)
        
        self._priv_sent += 1
    
    def wait_and_increment_join(self):
        """A utility method for waiting for the JOIN/AUTH limit to reset,
        and incrementing the counter.  If the counter is within the limit,
        the method will just increment the counter."""
        if self._join_sent >= self._join_limit:
            signals.wait_for_signal(self.on_join_limit_reset)
        
        self._join_sent += 1
    
    def reset_priv_limit(self, *, automated: bool = None):
        """Resets the PRIVMSG limit."""
        self._priv_sent = 0
        self.on_priv_limit_reset.emit()
        
        if automated:
            self._timer.singleShot(self._priv_period * 1000, self._reset_priv_limit_auto)
    
    def reset_join_limit(self, *, automated: bool = None):
        """Resets the JOIN/PASS limit."""
        self._join_sent = 0
        self.on_join_limit_reset.emit()
        
        if automated:
            self._timer.singleShot(self._join_period * 1000, self._reset_join_limit_auto)
    
    def reset_whisper_seconds(self, *, automated: bool = None):
        """Resets the whispers per second limit."""
        self._whispers_this_second = 0
        self.on_whisper_second_reset.emit()
        
        if automated:
            self._timer.singleShot(1000, self._reset_w_second_auto)
    
    def reset_whisper_minutes(self, *, automated: bool = None):
        """Resets the whispers per minute limit."""
        self._whispers_this_minute = 0
        self.on_whisper_minute_reset.emit()
        
        if automated:
            self._timer.singleShot(1000 * 60, self._reset_w_minute_auto)
        
        # Daily limit
        dif = self.whisper_reset - datetime.datetime.now(tz=datetime.timezone.utc)
        
        if dif.days > 0:
            self._whispered_accounts = 0
    
    def reset_whisper_daily(self, *, automated: bool = None):
        """Resets the account whisper limit."""
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        dif = self.whisper_reset - now
        
        if dif.days > 0:
            self._whispered_accounts = 0
            self.whisper_reset = now + datetime.timedelta(days=1)
            self.on_whisper_account_reset.emit()
            
            if automated:
                self._timer.singleShot(1000 * 60 * 60, self._reset_w_daily_auto)
    
    # Whisper Methods #
    def can_whisper(self, user: str) -> bool:
        """Returns whether or not the client is allows to send a whisper."""
        if user not in self._whispered_accounts and len(self._whispered_accounts) >= self._whisper_accounts_limit:
            return False
        
        elif self._whispers_this_minute >= self._whisper_minute_limit:
            return False
        
        elif self._whispers_this_second >= self._whisper_second_limit:
            return False
        
        else:
            return True
    
    def wait_for_whisper(self, *, include_accounts: bool = None):
        """Waits for the whisper limit to reset.  If `include_accounts` is true,
        this will also wait for the account limit to reset."""
        if self._whispers_this_minute >= self._whisper_minute_limit:
            signals.wait_for_signal(self.on_whisper_minute_reset)
        
        elif self._whispers_this_second >= self._whisper_second_limit:
            signals.wait_for_signal(self.on_whisper_second_reset)
        
        elif include_accounts and len(self._whispered_accounts) >= self._whisper_accounts_limit:
            signals.wait_for_signal(self.on_whisper_account_reset)
    
    def increment_whisper(self, user: str):
        """Increments the whisper internal ratelimit."""
        if user not in self._whispered_accounts:
            self._whispered_accounts.append(user)
        
        self._whispers_this_second += 1
        self._whispers_this_minute += 1
