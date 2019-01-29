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

from PyQt5 import QtGui

from ...enums import irc

__all__ = ['Tag', 'Badge']


@dataclasses.dataclass(frozen=True)
class Tag:
    """The base class for all tags."""
    __slots__ = ['tag', 'value']
    
    tag: str
    value: typing.Any


@dataclasses.dataclass(frozen=True)
class Badge(Tag):
    """A badge from an IRC message."""
    __slots__ = ['value']
    
    value: typing.List[typing.Tuple[typing.Union[irc.BadgeTypes, str], int]]
    tag: str = 'badges'


@dataclasses.dataclass(frozen=True)
class Bit(Tag):
    """A tag representing the bit information sent by Twitch."""
    __slots__ = ['value']
    
    value: int
    tag: str = 'bits'


@dataclasses.dataclass(frozen=True)
class Color(Tag):
    """A tag representing the color information sent by Twitch."""
    __slots__ = ['value']
    
    value: typing.Optional[QtGui.QColor]
    tag: str = 'color'


@dataclasses.dataclass(frozen=True)
class Emotes(Tag):
    """A tag representing the emote information sent by Twitch."""
    __slots__ = ['value']
    
    value: typing.Dict[str, typing.List[typing.Tuple]]
    tag: str = 'emotes'


@dataclasses.dataclass(frozen=True)
class DisplayName(Tag):
    """A tag representing the display name of the sender."""
    __slots__ = ['value']
    
    value: str
    tag: str = 'display-name'


@dataclasses.dataclass(frozen=True)
class Id(Tag):
    """A tag representing an ID."""
    __slots__ = ['value']
    
    value: str


@dataclasses.dataclass(frozen=True)
class Sent(Tag):
    """A tag representing the moment the server received the message."""
    __slots__ = ['value']
    
    value: datetime.datetime
    tag: str = 'tmi-sent-ts'


@dataclasses.dataclass(frozen=True)
class BroadcasterLang(Tag):
    """A tag representing the broadcaster's language."""
    __slots__ = ['value']
    
    value: str
    tag: str = 'broadcaster-lang'


@dataclasses.dataclass(frozen=True)
class EmoteOnly(Tag):
    """A tag indicating whether or not the current channel is in emote only."""
    __slots__ = ['value']
    
    value: int
    tag: str = 'emote-only'


@dataclasses.dataclass(frozen=True)
class FollowerOnly(Tag):
    """A tag indicating whether or not the current channel is in follower only."""
    __slots__ = ['value']
    
    value: int
    tag: str = 'followers-only'


@dataclasses.dataclass(frozen=True)
class R9K(Tag):
    """A tag indicating whether or not the current channel is in R9K mode."""
    __slots__ = ['value']
    
    value: int
    tag: str = 'r9k'


@dataclasses.dataclass(frozen=True)
class Slow(Tag):
    """A tag indicating whether or not the current channel is in slow mode."""
    __slots__ = ['value']
    
    value: int
    tag: str = 'slow'


@dataclasses.dataclass(frozen=True)
class SubOnly(Tag):
    """A tag indicating whether or not the current channel is in sub only mode."""
    __slots__ = ['value']
    
    value: int
    tag: str = 'subs-only'


@dataclasses.dataclass(frozen=True)
class Login(Tag):
    """A tag representing the user information sent by Twitch."""
    __slots__ = ['value']
    
    value: str
    tag: str = 'login'


@dataclasses.dataclass(frozen=True)
class Months(Tag):
    """A tag representing the amount of months a user was subscribed for."""
    __slots__ = ['value']
    
    value: int


@dataclasses.dataclass(frozen=True)
class Recipient(Tag):
    """A tag representing the recipient of a sub gift."""
    __slots__ = ['value']
    
    value: str
    tag: str = 'msg-param-recipient-display-name'
