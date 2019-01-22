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
import typing

from PyQt5 import QtCore, QtGui

from ...enums import api


class User(QtCore.QObject):
    """A user on Twitch."""
    onBanned = QtCore.pyqtSignal(object, str, int)  # Channel (User), reason, duration
    onSubscribed = QtCore.pyqtSignal(object)  # Channel
    onCheer = QtCore.pyqtSignal(int)  # Amount
    onModded = QtCore.pyqtSignal()
    onUnmodded = QtCore.pyqtSignal()
    
    def __init__(self, state, **kwargs):
        # Super Call #
        super(User, self).__init__(parent=kwargs.get('parent'))
        
        # "Private" Attributes #
        self._state = state
        self._login: str = kwargs.get('login')
        self._broadcaster_type: api.BroadcasterTypes = kwargs.get('broadcaster_type')
        self._description: str = kwargs.get('description')
        self._display_name: str = kwargs.get('display_name', self._login.title())
        self._email: typing.Optional[str] = kwargs.get('email')
        self._id: str = kwargs.get('id')
        self._offline_image_url: QtCore.QUrl = kwargs.get('offline_image_url')
        self._profile_image_url: QtCore.QUrl = kwargs.get('profile_image_url')
        self._type: api.UserTypes = kwargs.get('type')
        self._view_count: int = kwargs.get('view_count')
        
        # Chat Attributes
        self._nick_hex: QtGui.QColor = kwargs.get('nick_hex')
        self._emote_sets: typing.List[str] = kwargs.get('emote_sets')
        
        # Channel Attributes
        self._modded_in: typing.List[str] = list()
        self._subscriptions: typing.List[str] = list()
        self._badges: typing.Dict[str, typing.List[object]] = list()
        
        # Aliases #
        self.username = self.login
    
    # Properties #
    @property
    def login(self) -> str:
        """The user's username."""
        return self._login
    
    @property
    def display_name(self) -> str:
        """The user's name with custom capitalization."""
        return self._display_name
    
    @property
    def broadcaster_type(self) -> api.BroadcasterTypes:
        """The type of broadcaster the user is."""
        return self._broadcaster_type
    
    @property
    def description(self) -> str:
        """The user's channel description, or bio."""
        return self._description
    
    @property
    def email(self) -> typing.Optional[str]:
        """The user's email address."""
        return self._email
    
    @property
    def id(self) -> str:
        """The user's Twitch ID."""
        return self._id
    
    @property
    def type(self) -> api.UserTypes:
        """The type of user this user is."""
        return self._type
    
    @property
    def view_count(self) -> int:
        """The amount of views the user's channel has obtained."""
        return self._view_count
    
    # Channel Methods #
    @property
    def user_color(self) -> QtGui.QColor:
        """The color hex of the user's name as it appears in chat."""
        return self._nick_hex
    
    @user_color.setter
    def user_color(self, value: typing.Union[str, QtGui.QColor]):
        if isinstance(value, QtGui.QColor):
            self._nick_hex = value
        
        elif type(value) == str:
            if not value.startswith("#"):
                value = f'#{value}'
            
            self._nick_hex = QtGui.QColor(value)
    
    def is_mod(self, channel: str) -> bool:
        """Returns whether or not the user could be considered a
        moderator in a given channel."""
        return channel.lower() in self._modded_in
    
    def is_subbed(self, channel: str) -> bool:
        """Returns whether or not the user could be considered a
        subscriber in a given channel."""
        return channel.lower() in self._subscriptions
