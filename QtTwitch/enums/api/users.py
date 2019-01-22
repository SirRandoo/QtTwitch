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

__all__ = {"UserTypes", "BroadcasterTypes"}


class UserTypes(enum.Enum):
    """The different types of users."""
    USER = ''
    GLOBAL_MOD = 'global_mod'
    ADMIN = 'admin'
    STAFF = 'staff'
    
    # Aliases #
    GLOBAL_MODERATOR = GLOBAL_MOD
    ADMINISTRATOR = ADMIN


class BroadcasterTypes(enum.Enum):
    """The different types of broadcasters."""
    NONE = ''
    AFFILIATE = 'affiliate'
    PARTNER = 'partner'
