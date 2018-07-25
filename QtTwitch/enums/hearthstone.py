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
#
# These enumerations are probably overkill
# since Hearthstone or Twitch can make any
# of these enums invalid.
import enum


class Classes(enum.Enum):
    """The list of Hearthstone classes currently
    supported by the Twitch metadata API."""
    DRUID = enum.auto()
    HUNTER = enum.auto()
    MAGE = enum.auto()
    PALADIN = enum.auto()
    PRIEST = enum.auto()
    ROGUE = enum.auto()
    SHAMAN = enum.auto()
    WARLOCK = enum.auto()
    WARRIOR = enum.auto()
    
    def __call__(self, value):
        if isinstance(value, str):
            if value.upper() in self._member_names_:
                return self._member_map_[value.upper()]


class Mode(enum.Enum):
    """The list of modes currently in Hearthstone."""
    CASUAL = enum.auto()
    ARENA = enum.auto()
    ADVENTURE = enum.auto()
    TAVERN = enum.auto()
    
    def __call__(self, value):
        if isinstance(value, str):
            if value.upper() in self._member_names_:
                return self._member_map_[value.upper()]
