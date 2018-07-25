# This file is part of Decision Descent: Client.
#
# Decision Descent: Client is free software:
# you can redistribute it and/or
# modify it under the terms of the 
# GNU General Public License as 
# published by the Free Software 
# Foundation, either version 3 of 
# the License, or (at your option) 
# any later version.
#
# Decision Descent: Client is 
# distributed in the hope that it 
# will be useful, but WITHOUT ANY 
# WARRANTY; without even the implied 
# warranty of MERCHANTABILITY or 
# FITNESS FOR A PARTICULAR PURPOSE.  
# See the GNU General Public License 
# for more details.
#
# You should have received a copy of
# the GNU General Public License along 
# with Decision Descent: Client.  
# If not, see <http://www.gnu.org/licenses/>.
import logging
import random
import re

from PyQt5 import QtNetwork, QtCore
from QtUtilities import signals
from .dataclasses.qmessage import QMessage

logger = logging.getLogger(__name__)


__all__ = {"IRC"}


class IRC(QtCore.QObject):
    """A class for interacting with Twitch's IRC."""
    on_message = QtCore.pyqtSignal(object)
    
    def __init__(self, nickname: str=None, token: str=None, channel: str=None, parent: QtCore.QObject=None):
        # Super Call #
        super(IRC, self).__init__(parent=parent)
        
        # "Public" Attributes #
        self.qt_disconnect = super(IRC, self).disconnect
        
        # "Private" Attributes #
        self._token = token
        self._nick = nickname
        self._channel = channel

        self._host = "irc.chat.twitch.tv"
        self._port = 443

        self._messages_sent, self._message_limit = 0, 20
        self._socket = QtNetwork.QSslSocket(parent=self)
        self._timer = QtCore.QTimer(parent=self)
        self._tag_regex = re.compile("@(?P<tags>.*) :(?P<name>\w+)!(?P=name)@(?P=name)\.\w+\.\w+\.\w+ PRIVMSG"
                                     " #(?P<channel>[a-zA-Z0-1_]+) :(?P<message>.*)")
        
        # Internal Calls #
        self._socket.encrypted.connect(self._continue_connection)
        self._timer.timeout.connect(self._reset_message_limit)
        self._socket.readyRead.connect(self._message_ready)
    
    # Credential Methods #
    def set_credentials(self, nick: str=None, token: str=None):
        """Sets the credentials this connection will use."""
        if nick is None or token is None:
            nick = "justinfan{}".format(str(random.randint(9999)))
            token = None
        
        if self._token != token or self._nick != nick:
            self.disconnect()
            self.connect()
            
        self._token = token
        self._nick = nick
    
    def set_channel(self, channel: str=None):
        """Sets the channel this connection will use."""
        if channel is None:
            if self._socket.isValid():
                self.send_raw_message(f"PART #{self._channel}")
                
            self._channel = None
        
        else:
            if self._socket.isValid():
                self.send_raw_message(f"PART #{self._channel}")
                
            self._channel = channel
            
            if self._socket.isValid():
                self.send_raw_message(f"JOIN #{self._channel}")
    
    def can_connect(self):
        """Returns whether or not the connection can successfully connect to
        a channel."""
        if self._nick is None:
            return False

        elif self._nick.startswith("justinfan"):
            return True

        if self._token is None:
            return False
        
        if self._channel is None:
            return False
        
        return True
    
    # Connection Methods #
    def connect(self, host: str=None, port: int=None):
        """Connects to Twitch's IRC servers."""
        if host is not None:
            self._host = host

        if port is not None:
            self._port = port
        
        if self.can_connect():
            self._socket.connectToHostEncrypted(self._host, self._port)
            
        else:
            raise ConnectionAbortedError("A channel, valid token, and nick is required!  "
                                         "calling `set_credentials` without specifying "
                                         "arguments will enable the connection to connect "
                                         "anonymously, but a channel must be specified.")
    
    def _continue_connection(self):
        """Continues connecting to Twitch's IRC servers."""
        self._timer.start(30 * 1000)
        if self._token is not None:
            self.send_raw_message(f"PASS {self._token}")
        
        elif self._nick.startswith("justinfan"):
            self.send_raw_message(f"PASS justinfan")  # Not needed, but eh
        
        self.send_raw_message(f"NICK {self._nick}")
        self.send_raw_message(f"JOIN #{self._channel}")
        self.send_raw_message("CAP REQ :twitch.tv/tags")
        self.send_raw_message("CAP REQ :twitch.tv/membership")
        self.send_raw_message("CAP REQ :twitch.tv/commands")
    
    def disconnect(self):
        """Disconnects from Twitch's IRC."""
        if self._socket.isValid():
            self._socket.disconnect()
    
    # Communication Methods #
    def send_raw_message(self, message: str):
        if self._messages_sent < self._message_limit:
            if not message.endswith("\r\n"):
                message += "\r\n"
            
            self._socket.write(message.encode())
            # print(message, end="")
            
        else:
            logger.warning("Message limit hit!")
    
    def send_message(self, message: str):
        """Sends a PRIVMSG to Twitch's IRC server."""
        self.send_raw_message(f"PRIVMSG #{self._channel} :{message}")
    
    # Slots #
    def _reset_message_limit(self):
        """Resets the internal message counter."""
        self._messages_sent = 0
    
    def _message_ready(self):
        """Called whenever the socket receives a new message."""
        if self._socket.isReadable():
            data = self._socket.readAll()
            
            if not data.isNull() or not data.isEmpty():
                data = data.data().decode()
                
                for line in data.splitlines():
                    if line == "PING :tmi.twitch.tv\r\n":
                        self.send_raw_message("PONG :tmi.twitch.tv")

                    elif line == ":tmi.twitch.tv RECONNECT":
                        logger.warning("Received RECONNECT notice...")
                        self.disconnect()
                        self._timer.singleShot(5000, self.connect)  # Reconnect after 5 seconds
                    
                    bits = self._tag_regex.match(line)
                    
                    if bits:
                        message = QMessage.from_match(bits.groupdict())
                        
                        if message == self._nick:
                            self._messages_sent += 1  # We do this since Twitch's IRC limits are account based
                        
                        self.on_message.emit(message)
