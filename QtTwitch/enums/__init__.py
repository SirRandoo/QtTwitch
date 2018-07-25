# This file is part of QtTwitch.
#
# QtTwitch is free software: you can
# redistribute it and/or modify it
# under the terms of the GNU Lesser
# General Public License as published
# by the Free Software Foundation,
# either version 3 of the License, or
# (at your option) any later version.
#
# QtTwitch is distributed in the hope
# that it will be useful, but WITHOUT
# ANY WARRANTY; without even the
# implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of
# the GNU Lesser General Public License
# along with QtTwitch.  If not, see
# <http://www.gnu.org/licenses/>.
#
# Author: RandomShovel
# File Date: 11/14/2017
import enum

from . import hearthstone, overwatch


class StreamTypes(enum.Enum):
    """The different types of streams on Twitch."""
    LIVE = enum.auto()
    VODCAST = enum.auto()
    PLAYLIST = enum.auto()
    UNKNOWN = enum.auto()
    
    def __call__(self, value):
        if isinstance(value, str):
            if value.upper() in self._member_names_:
                return self._member_map_[value.upper()]
    
    def _missing_(*args):
        return StreamTypes.UNKNOWN


class UserTypes(enum.Enum):
    """The different types of users on Twitch."""
    STAFF = enum.auto()
    ADMIN = enum.auto()
    GLOBAL_MOD = enum.auto()
    
    BROADCASTER = enum.auto()
    MOD = enum.auto()
    USER = enum.auto()
    
    def __call__(self, value):
        if isinstance(value, str):
            if value.upper() in self._member_names_:
                return self._member_map_[value.upper()]
    
    def __missing__(*args):
        return UserTypes.USER


class BroadcasterTypes(enum.Enum):
    """The different types of broadcasters on Twitch."""
    PARTNER = enum.auto()
    AFFILIATE = enum.auto()
    DEFAULT = enum.auto()
    
    def __call__(self, value):
        if isinstance(value, str):
            if value.upper() in self._member_names_:
                return self._member_map_[value.upper()]
    
    def _missing_(*args):
        return BroadcasterTypes.DEFAULT
