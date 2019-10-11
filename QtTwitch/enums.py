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
import enum

__all__ = ['ExtensionTypes']


class ExtensionTypes(enum.Enum):
    """The different types of extensions."""
    COMPONENT = 'component'
    MOBILE = 'mobile'
    PANEL = 'panel'
    OVERLAY = 'overlay'


class HearthClasses(enum.Enum):
    """The list of Hearthstone classes currently supported by the Twitch
    metadata api."""
    DRUID = 'druid'
    HUNTER = 'hunter'
    MAGE = 'mage'
    PALADIN = 'paladin'
    PRIEST = 'priest'
    ROGUE = 'rogue'
    SHAMAN = 'shaman'
    WARLOCK = 'warlock'
    WARRIOR = 'warrior'


class OverwatchRoles(enum.Enum):
    """The different hero roles currently in Overwatch."""
    OFFENSE = 'offense'
    DEFENSE = 'defense'
    TANK = 'tank'
    SUPPORT = 'support'


class UserTypes(enum.Enum):
    """The different types of users."""
    USER = ''
    GLOBAL_MOD = 'global_mod'
    ADMIN = 'admin'
    STAFF = 'staff'
    
    # Aliases
    GLOBAL_MODERATOR = GLOBAL_MOD
    ADMINISTRATOR = ADMIN


class BroadcasterTypes(enum.Enum):
    """The different types of broadcasters."""
    NONE = ''
    AFFILIATE = 'affiliate'
    PARTNER = 'partner'


class VideoTypes(enum.Enum):
    """The different types of videos."""
    UPLOAD = 'upload'
    HIGHLIGHT = 'highlight'
    ARCHIVE = 'archive'


class VideoVisibilities(enum.Enum):
    """The different types of video visibilities."""
    PUBLIC = 'public'
    PRIVATE = 'private'


class BadgeTypes(enum.Enum):
    """The different types of badges a user can have."""
    ADMIN = 'admin'
    BITS = 'bits'
    BROADCASTER = 'broadcaster'
    GLOBAL_MOD = 'global_mod'
    MODERATOR = 'moderator'
    SUBSCRIBER = 'subscriber'
    STAFF = 'staff'
    TURBO = 'turbo'
    PREMIUM = 'premium'
    CHARITY = 'bits-charity'
    VIP = 'vip'
    LEADER = 'bits-leader'
    
    # Alias
    GLOBAL_MODERATOR = GLOBAL_MOD
    MOD = MODERATOR
    SUB = SUBSCRIBER
    PRIME = PREMIUM


class MessageIds(enum.Enum):
    """The various message ids a Twitch message can contain."""
    SUB = 'sub'
    RESUB = 'resub'
    SUB_GIFT = 'subgift'
    ANON_SUB_GIFT = 'anonsubgift'
    RAID = 'raid'
    RITUAL = 'ritual'
    
    # Aliases
    ANONYMOUS_SUB_GIFT = ANON_SUB_GIFT
    ANONYMOUS_SUBSCRIBER_GIFT = ANON_SUB_GIFT
    
    SUBSCRIBER = SUB
    SUBSCRIBER_GIFT = SUB_GIFT
    RESUBSCRIBER = RESUB


class SubPlans(enum.Enum):
    """The various sub plans."""
    PRIME = 'Prime'
    FIRST = 1000
    SECOND = 2000
    THIRD = 3000


class SysMessageTypes(enum.Enum):
    """The various system message Twitch can send."""
    GENERIC = enum.auto()  # Generic IRC spec responses
    
    PING = enum.auto()
    JOIN = enum.auto()
    PART = enum.auto()
    CAP = enum.auto()
    MODE = enum.auto()
    NAMES = enum.auto()
    CLEAR_CHAT = enum.auto()
    CLEAR_MSG = enum.auto()
    HOST_TARGET = enum.auto()
    NOTICE = enum.auto()
    RECONNECT = enum.auto()
    ROOM_STATE = enum.auto()
    USER_NOTICE = enum.auto()
    USER_STATE = enum.auto()
    GLOBAL_USER_STATE = enum.auto()


class MessageTypes(enum.Enum):
    """The various types of messages Twitch's IRC servers can send."""
    SYSTEM = enum.auto()
    ACKNOWLEDGEMENT = enum.auto()
    JOIN = enum.auto()
    ROOM_STATE = enum.auto()
    HOST_TARGET = enum.auto()
    NOTICE = enum.auto()
    NAMES = enum.auto()
    NAMES_END = enum.auto()
    MODE = enum.auto()
    PRIVATE_MESSAGE = enum.auto()
    PART = enum.auto()
    USER_NOTICE = enum.auto()
    
    PRIVMSG = PRIVATE_MESSAGE
    ACK = ACKNOWLEDGEMENT


class IrcResponses(enum.Enum):
    WELCOME = 1
    YOUR_HOST = 2
    CREATED = 3
    MY_INFO = 4
    
    MOTD_START = 375
    MOTD = 372
    MOTD_END = 276
    
    NAME_REPLY = 353
    NAME_END = 366
    
    UNKNOWN_COMMAND = 421
