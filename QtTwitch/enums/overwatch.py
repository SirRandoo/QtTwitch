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


class Roles(enum.Enum):
    """The different hero roles currently in Overwatch."""
    OFFENSE = enum.auto()
    DEFENSE = enum.auto()
    TANK = enum.auto()
    SUPPORT = enum.auto()

    def __call__(self, value):
        if isinstance(value, str):
            if value.upper() in self._member_names_:
                return self._member_map_[value.upper()]
