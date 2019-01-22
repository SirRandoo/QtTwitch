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
import collections
import datetime
import typing

from PyQt5 import QtGui

from enums import irc

SimpleBadge = collections.namedtuple('SimpleBadge', ['badge', 'version'])


class UserState:
    """A class for housing state related data."""
    
    def __init__(self, **kwargs):
        self._login: str = kwargs.get('login')
        self._user_id: str = kwargs.get('user_id')
        self._channel: str = kwargs.get('channel')  # Just in case?
        
        self._display_name: str = kwargs.get('display_name')
        self._name_color: QtGui.QColor = kwargs.get('color')
        self._badges: typing.List[SimpleBadge] = kwargs.get('badges', [])
        self._emote_sets: typing.List[str] = kwargs.get('emote_sets', [])
        
        self._sent_ts: datetime.datetime = None
        self._mod: bool = self.is_mod()
        self._sub: bool = self.is_sub()
        self._turbo: bool = self.is_turbo()
        self._user_type: irc.UserTypes = irc.UserTypes(kwargs.get('user_type', ''))
        
        # Conversion
        if 'tmi_sent_ts' in kwargs:
            self._sent_ts = datetime.datetime.fromtimestamp(kwargs.get('tmi_sent_ts'), tz=datetime.timezone.utc)
    
    # Properties #
    def is_mod(self) -> bool:
        """Whether or not the user is moderated."""
        return any([b.badge == 'moderator' for b in self._badges])
    
    def is_staff(self) -> bool:
        """Whether or not the user is a staff member."""
        return any([b.badge == 'staff' for b in self._badges])
    
    def is_turbo(self) -> bool:
        """Whether or not the user is a turbo user."""
        return any([b.badge == 'turbo' for b in self._badges])
    
    def is_vip(self) -> bool:
        """Whether or not the user is a VIP."""
        return any([b.badge == 'vip' for b in self._badges])
    
    def is_sub(self) -> bool:
        """Whether or not the user is a subscriber."""
        return any([b.badge == 'subscriber' for b in self._badges])
    
    def is_admin(self) -> bool:
        """Whether or not the user is an admin."""
        return any([b.badge == 'admin' for b in self._badges])
    
    def is_global_mod(self) -> bool:
        """Whether or not the user is a global mod."""
        return any([b.badge == 'global_mod' for b in self._badges])
    
    def is_broadcaster(self) -> bool:
        """Whether or not the user is the broadcaster."""
        return any([b.badge == 'broadcaster' for b in self._badges])
    
    def has_cheered(self) -> bool:
        """Whether or not the user has cheered."""
        return any([b.badge == 'bits' for b in self._badges])
    
    @property
    def color(self) -> typing.Optional[QtGui.QColor]:
        """The color the user's name will be displayed in.  If this is None,
        the user has not set a color yet."""
        return self._name_color
    
    @property
    def emote_sets(self) -> typing.List[str]:
        """The emote sets the user has available."""
        return self._emote_sets
    
    @property
    def display_name(self) -> typing.Optional[str]:
        """The formatted username of the user.  If this is None, the user has
        not set a display name yet."""
        return self._display_name
    
    @property
    def user_type(self) -> irc.UserTypes:
        """The user type for this user."""
        return self._user_type
    
    @property
    def sent_ts(self) -> typing.Optional[datetime.datetime]:
        """The moment Twitch's servers received the message accompanying this
        state."""
        return self._sent_ts
