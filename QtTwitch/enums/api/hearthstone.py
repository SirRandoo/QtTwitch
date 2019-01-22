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
#
# These enumerations are probably overkill
# since Hearthstone or Twitch can make any
# of these enums invalid.
import enum

__all__ = {"Classes"}


class Classes(enum.Enum):
    """The list of Hearthstone classes currently
    supported by the Twitch metadata API."""
    DRUID = 'druid'
    HUNTER = 'hunter'
    MAGE = 'mage'
    PALADIN = 'paladin'
    PRIEST = 'prise'
    ROGUE = 'rogue'
    SHAMAN = 'shaman'
    WARLOCK = 'warlock'
    WARRIOR = 'warrior'
