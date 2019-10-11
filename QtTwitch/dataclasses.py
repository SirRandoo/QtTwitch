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
import dataclasses
import datetime
import typing

from PyQt5 import QtCore, QtGui

from . import enums, errors

if typing.TYPE_CHECKING:
    from .client import Client

__all__ = ['SystemMessage', 'Community', 'Channel', 'PrivateMessage',
           'Game', 'Stream', 'StreamTag', 'User', 'Video']


@dataclasses.dataclass(frozen=True)
class SystemMessage:
    """A message from a Twitch's IRC server, excluding PRIVMSGs."""
    type: enums.SysMessageTypes
    user: typing.Optional[str]
    message: typing.Optional[str]
    code: typing.Optional[enums.IrcResponses]


@dataclasses.dataclass(frozen=True)
class ModeMessage(SystemMessage):
    """A MODE message from Twitch's IRC server."""
    user: str
    channel: str
    op: bool
    
    def __init__(self, channel: str, user: str, op: bool):
        super(ModeMessage, self).__init__(type=enums.SysMessageTypes.MODE, user=user)
        
        # Set the classes' attributes
        object.__setattr__(self, 'channel', channel)
        object.__setattr__(self, 'op', op)


@dataclasses.dataclass(frozen=True)
class NamesMessage(SystemMessage):
    """A NAMES message from Twitch's IRC server."""
    channel: str
    names: typing.List[str]
    
    def __init__(self, channel: str, names: typing.List[str]):
        super(NamesMessage, self).__init__(type=enums.SysMessageTypes.NAMES, code=enums.IrcResponses.NAME_REPLY)
        
        # Set the classes' attributes
        object.__setattr__(self, 'channel', channel)
        object.__setattr__(self, 'names', names)


@dataclasses.dataclass(frozen=True)
class JoinMessage(SystemMessage):
    """A JOIN message from Twitch's IRC server."""
    user: str
    channel: str
    
    def __init__(self, channel: str, user: str):
        super(JoinMessage, self).__init__(type=enums.SysMessageTypes.JOIN, user=user)
        
        # Set the classes' attributes
        object.__setattr__(self, 'channel', channel)


@dataclasses.dataclass(frozen=True)
class PartMessage(SystemMessage):
    """A PART message from Twitch's IRC server."""
    user: str
    channel: str
    
    def __init__(self, channel: str, user: str):
        super(PartMessage, self).__init__(type=enums.SysMessageTypes.PART, user=user)
        
        # Set the classes' attributes
        object.__setattr__(self, 'channel', channel)


@dataclasses.dataclass(frozen=True)
class HostMessage(SystemMessage):
    """A HOSTTARGET message from Twitch's IRC server."""
    channel: str
    
    def __init__(self, channel: str, user: str):
        super(HostMessage, self).__init__(type=enums.SysMessageTypes.HOST_TARGET, user=user)
        
        # Set the classes' attributes
        object.__setattr__(self, 'channel', channel)


@dataclasses.dataclass(frozen=True)
class ClearChatMessage(SystemMessage):
    """A CLEARCHAT message from Twitch's IRC server."""
    channel: str
    
    def __init__(self, channel: str):
        super(ClearChatMessage, self).__init__(type=enums.SysMessageTypes.CLEAR_CHAT)
        
        # Set the classes' attributes
        object.__setattr__(self, 'channel', channel)


@dataclasses.dataclass(frozen=True)
class ClearMsgMessage(SystemMessage):
    """A message specific CLEARCHAT message from Twitch's IRC server."""
    channel: str
    message_id: str
    
    def __init__(self, channel: str, message_id: str):
        super(ClearMsgMessage, self).__init__(type=enums.SysMessageTypes.CLEAR_MSG)
        
        # Set the classes' attributes
        object.__setattr__(self, 'channel', channel)
        object.__setattr__(self, 'message_id', message_id)


@dataclasses.dataclass(frozen=True)
class Channel:
    """A class for housing channel info."""
    state: 'Client'
    
    name: str
    display_name: typing.Optional[str]
    email: typing.Optional[str]
    id: str
    
    views: int
    offline_image_url: typing.Optional[QtCore.QUrl]
    profile_image_url: typing.Optional[QtCore.QUrl]
    
    type: enums.UserTypes
    broadcaster_type: enums.BroadcasterTypes
    description: typing.Optional[str]
    
    viewers: typing.List['User']
    
    # Getters
    def client(self) -> 'User':
        """Returns the client's User object for this channel."""
        for v in self.viewers:
            if v.channel.name == self.state.irc.nick:
                return v
        
        raise LookupError
    
    def moderators(self) -> typing.List['User']:
        """The current list of moderators in this channel."""
        return [v for v in self.viewers if v.is_operator()]
    
    def vips(self) -> typing.List['User']:
        """The current list of VIPs in this channel."""
        return [v for v in self.viewers]
    
    # Commands
    def clear(self):
        """Clears the chat.
        
        :raises LookupError: The client could not be found in the channel.
        :raises PermissionError: The client does not have permission to use this
        command."""
        if not self.client().is_operator():
            raise PermissionError
        
        self.state.irc.clear(channel=self.name)
    
    def ban(self, user: 'User', reason: str = None):
        """Bans a user from this channel.
        
        :raises LookupError: The client could not be found in the channel.
        :raises PermissionError: The client does not have permission to use this
        command."""
        if not self.client().is_operator():
            raise PermissionError
        
        self.state.irc.ban(channel=self.name, user=user.name, reason=reason)
    
    def unban(self, user: 'User'):
        """Unbans a user from a channel.
        
        :raises LookupError: The client could not be found in this channel.
        :raises PermissionError: The client does not have permission to use this
        command."""
        if not self.client().is_operator():
            raise PermissionError
        
        self.state.irc.unban(channel=self.name, user=user.name)
    
    def timeout(self, user: 'User', duration: int = None, reason: str = None):
        """Times out a user in a channel.
        
        :raises LookupError: The client could not be found in this channel.
        :raises PermissionError: The client does not have permission to use this
        command."""
        if not self.client().is_operator():
            raise PermissionError
        
        self.state.irc.timeout(channel=self.name, user=user.name, duration=duration, reason=reason)
    
    def me(self, message: str):
        """Sends a /client message to this channel.
        
        :raises LookupError: The client could not be found this channel."""
        if self.client():
            self.state.irc.me(channel=self.name, text=message)
    
    def join(self):
        """Joins this channel.
        
        :raises ChannelError: The client is already in the channel."""
        if self.name in self.state.irc.channels:
            raise errors.ChannelError(f'Already in channel #{self.name}')
        
        self.state.irc.join(self.name)
    
    def leave(self):
        """Leaves this channel.
        
        :raises ChannelError: The client is not in the channel."""
        if self.name not in self.state.irc.channels:
            raise errors.ChannelError(f'Not in channel #{self.name}')
        
        self.state.irc.part(channel=self.name)
    
    def slow(self, seconds: int = None):
        """Enables slow mode.  If seconds is specified, messages can only be
        sent once per period.
        
        :raises LookupError: The client is not in the channel.
        :raises PermissionError: The client does not have permission to use this
        command."""
        if not self.client().is_operator():
            raise PermissionError
        
        self.state.irc.slow(channel=self.name, limit=seconds)
    
    def slowoff(self):
        """Disables slow mode in this channel.
        
        :raises LookupError: The client is not in the channel.
        :raises PermissionError: The client does not have permission to use this
        command."""
        if not self.client().is_operator():
            raise PermissionError
        
        self.state.irc.slowoff(channel=self.name)
    
    def followers_only(self, *, mins: int = None, hrs: int = None,
                       days: int = None, wks: int = None, mnths: int = None):
        """Enables follower only mode in this channel.
        
        :raises LookupError: The client is not in this channel.
        :raises PermissionError: The client does not have permission to use this
        command."""
        if not self.client().is_operator():
            raise PermissionError
        
        self.state.irc.followers(channel=self.name, mins=mins, hrs=hrs, days=days, wks=wks, mnths=mnths)
    
    def followersoff(self):
        """Disables follower only mode in this channel.
        
        :raises LookupError: The client is not in this channel.
        :raises PermissionError: The client does not have permission to use this
        command."""
        if not self.client().is_operator():
            raise PermissionError
        
        self.state.irc.followersoff(channel=self.name)
    
    def subscribers_only(self):
        """Enables subscriber only mode in this channel.
        
        :raises LookupError: The client is not in this channel.
        :raises PermissionError: The client does not have permission to use this
        command."""
        if not self.client().is_operator():
            raise PermissionError
        
        self.state.irc.subscribers(channel=self.name)
    
    def subscribersoff(self):
        """Disables subscriber only mode in this channel.
        
        :raises LookupError: The client is not in this channel.
        :raises PermissionError: The client does not have permission to use this
        command."""
        if not self.client().is_operator():
            raise PermissionError
        
        self.state.irc.subscribersoff(channel=self.name)
    
    def r9kbeta(self):
        """Enables R9K beta in this channel.
        
        :raises LookupError: The client is not in this channel.
        :raises PermissionError: The client does not have permission to use this
        command."""
        if not self.client().is_operator():
            raise PermissionError
        
        self.state.irc.r9kbeta(channel=self.name)
    
    def r9kbetaoff(self):
        """Disables R9K beta in this channel.
        
        :raises LookupError: The client is not in this channel.
        :raises PermissionError: The client does not have permission to use this
        command."""
        if not self.client().is_operator():
            raise PermissionError
        
        self.state.irc.r9kbetaoff(channel=self.name)
    
    def emoteonly(self):
        """Enables emote only mode in this channel.
        
        :raises LookupError: The client is not in this channel.
        :raises PermissionError: The client does not have permission to use this
        command."""
        if not self.client().is_operator():
            raise PermissionError
        
        self.state.irc.emoteonly(channel=self.name)
    
    def emoteonlyoff(self):
        """Disables emote only mode for this channel.
        
        :raises LookupError: The client is not in this channel.
        :raises PermissionError: The client does not have permission to use this
        command."""
        if not self.client().is_operator():
            raise PermissionError
        
        self.state.irc.emoteonlyoff(channel=self.name)
    
    def mod(self, user: 'User'):
        """Promotes a user to moderator.
        
        :raises LookupError: The client is not in the channel.
        :raises ValueError: The user specified is already a moderator.
        :raises PermissionError: The client does not have permission to use this
        command."""
        if not self.client().is_operator():
            raise PermissionError
        
        if user.name in [u.name for u in self.moderators()]:
            raise ValueError
        
        self.state.irc.mod(channel=self.name, user=user.name)
    
    def unmod(self, user: 'User'):
        """Demotes a moderator in this channel.
        
        :raises LookupError: The client is not in the channel.
        :raises ValueError: The user specified is not a moderator.
        :raises PermissionError: The client does not have permission to use this
        command."""
        if not self.client().is_operator():
            raise PermissionError
        
        if user.name not in [u.name for u in self.moderators()]:
            raise ValueError
        
        self.state.irc.unmod(channel=self.name, user=user.name)
    
    def host(self, channel: 'Channel'):
        """Hosts a channel.
        
        :raises LookupError: The client is not in the channel.
        :raises PermissionError: The client does not have permission to use this
        command."""
        if not self.client().is_operator():
            raise PermissionError
        
        self.state.irc.host(channel=self.name, target=channel.name)
    
    def unhost(self):
        """Exits host mode for this channel.
        
        :raises LookupError: The client is not in this channel.
        :raises PermissionError: The client does not have permission to use this
        command."""
        if not self.client().is_operator():
            raise PermissionError
        
        self.state.irc.unhost(channel=self.name)
    
    def vip(self, user: 'User'):
        """Promotes a user to VIP.
        
        :raises LookupError: The client is not in this channel.
        :raises ValueError: The user specified is already a VIP.
        :raises PermissionError: The client does not have permission to use this
        command."""
        if not self.client().is_operator():
            raise PermissionError
        
        self.state.irc.vip(channel=self.name, user=user.name)
    
    def unvip(self, user: 'User'):
        """Demotes a VIP.
        
        :raises LookupError: The client is not in this channel.
        :raises ValueError: The user specified is not a VIP.
        :raises PermissionError: The client does not have permission to use this
        command."""
        if not self.client().is_operator():
            raise PermissionError
        
        if not any([b.type == enums.BadgeTypes.VIP for b in user.badges]):
            raise ValueError
        
        self.state.irc.unvip(channel=self.name, user=user.name)
    
    def delete(self, message: 'PrivateMessage'):
        """Deletes a private message.
        
        :raises ValueError: The client is not in this channel.
        :raises PermissionError: The client does not have permission to use this
        command."""
        if not self.client().is_operator():
            raise PermissionError
        
        self.state.irc.delete(channel=self.name, message_id=message.id)


@dataclasses.dataclass(frozen=True)
class Community:
    """A class for housing community related data."""


@dataclasses.dataclass(frozen=True)
class Emote:
    """A class for housing emote related data."""
    code: str
    
    id: typing.Optional[int]
    set: typing.Optional[int]
    
    def __str__(self):
        return self.code


@dataclasses.dataclass(frozen=True)
class Video:
    """A class for housing video related data."""
    id: str
    title: str
    type: enums.VideoTypes
    description: typing.Optional[str]
    duration: str
    language: str
    
    created_at: datetime.datetime
    published_at: datetime.datetime
    
    user: 'User'
    views: int
    visibility: enums.VideoVisibilities
    
    url: QtCore.QUrl
    thumbnail_url: QtCore.QUrl


@dataclasses.dataclass(frozen=True)
class StreamTag:
    """A class for housing stream tag data."""
    id: str
    auto: bool
    
    descriptions: typing.Dict[str, str]
    names: typing.Dict[str, str]


@dataclasses.dataclass(frozen=True)
class Game:
    """A class for housing game related data."""
    id: str
    name: str
    box_art_url: QtCore.QUrl


@dataclasses.dataclass(frozen=True)
class Stream:
    """A class for housing stream related information."""
    channel: Channel
    
    communities: typing.List[Community]
    game: Game
    id: str
    language: str
    started_at: datetime.datetime
    
    tags: typing.List[object]
    thumbnail_url: typing.Optional[QtCore.QUrl]
    
    title: str
    type: str
    
    user_id: str
    viewers: typing.List['User']


@dataclasses.dataclass(frozen=True)
class User:
    """A class for housing user info."""
    id: str
    name: str
    display_name: typing.Optional[str]
    
    badge_info: typing.Dict[str, typing.Any]
    badges: typing.List['Badge']
    color: typing.Optional[QtGui.QColor]
    emote_sets: typing.List[str]
    channel: typing.Optional[Channel]
    state: typing.Optional[object]
    
    def __post_init__(self):
        # Ensure the dataclasses' attributes exist
        try:
            self.display_name
        
        except AttributeError:
            object.__setattr__(self, 'display_name', self.name.title())
        
        try:
            self.channel
        
        except AttributeError:
            object.__setattr__(self, 'channel', None)
        
        try:
            self.state
        
        except AttributeError:
            object.__setattr__(self, 'state', None)
        
        try:
            self.color
        
        except AttributeError:
            object.__setattr__(self, 'color', None)
    
    def is_operator(self) -> bool:
        """Whether or not this user is a moderator."""
        for badge in self.badges:
            if badge.type in [enums.BadgeTypes.MODERATOR, enums.BadgeTypes.GLOBAL_MODERATOR, enums.BadgeTypes.STAFF,
                              enums.BadgeTypes.ADMIN, enums.BadgeTypes.BROADCASTER]:
                return True
        
        return False


@dataclasses.dataclass(frozen=True)
class Badge:
    """A class for housing badge data."""
    type: enums.BadgeTypes
    version: int


@dataclasses.dataclass(frozen=True)
class PrivateMessage:
    """A PRIVMSG message from a Twitch's IRC server."""
    content: str
    author: User
    channel: Channel
    id: str
    bits: typing.Optional[int]
    emotes: typing.List[Emote]
