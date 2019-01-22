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
import re
import typing

from PyQt5 import QtGui

from .state import SimpleBadge, UserState
from ..api import Cheermote, Emoticon, User


class PrivateMessage:
    """A chat message from Twitch."""
    
    # Regex
    REGEX = re.compile(r'@(?P<tags>.*) :(?P<name>\w+)!(?P=name)@(?P=name)\.\w\.w\.\w+ PRIVMSG #(?P<channel>\w+]) '
                       r':(?P<message>.*)')
    
    def __init__(self, state, **kwargs):
        # "Private" Attributes #
        self._state = UserState(**kwargs)
        
        self._content: str = kwargs.get("message")
        self._author: User = kwargs.get("author")
        self._channel: User = kwargs.get("channel")
        self._message_id: str = kwargs.get("id")
        self._bits: typing.Optional[Cheermote] = kwargs.get("bits")
        self._emotes: typing.Optional[typing.List[Emoticon]] = kwargs.get('emotes')
    
    # Properties #
    def is_cheer(self) -> bool:
        """Whether or not this message contains a cheer."""
        return bool(self._bits)
    
    @property
    def content(self) -> str:
        """The message the author sent."""
        return self._content
    
    @property
    def author(self) -> User:
        """The user that sent this message."""
        return self._author
    
    @property
    def message_id(self) -> str:
        """The id of this message."""
        return self._message_id
    
    # Wrapper Methods #
    def from_mod(self) -> bool:
        """Whether or not the message came from a moderator."""
        return self._state.is_mod()
    
    def from_sub(self) -> bool:
        """Whether or not the message came from a subscriber."""
        return self._state.is_sub()
    
    def from_turbo(self) -> bool:
        """Whether or not the message came from a turbo user."""
        return self._state.is_turbo()
    
    def from_broadcaster(self) -> bool:
        """Whether or not the message came from the broadcaster."""
        return self._state.is_broadcaster()
    
    def from_staff(self) -> bool:
        """Whether or not the message came from a Twitch staff member."""
        return self._state.is_staff()
    
    def from_admin(self) -> bool:
        """Whether or not the message came from an admin."""
        return self._state.is_admin()
    
    def from_global_mod(self) -> bool:
        """Whether or not the message came from a global moderator."""
        return self._state.is_global_mod()
    
    def from_vip(self) -> bool:
        """Whether or not the message came from a vip."""
        return self._state.is_vip()
    
    # Class Methods #
    @classmethod
    def from_message(cls, state, message: str) -> 'PrivateMessage':
        """Converts a raw IRC message into a Message object."""
        match = cls.REGEX.match(message)
        
        if match:
            data = match.groupdict()
            
            if state is None:
                state = UserState(
                    badges=[SimpleBadge(*b.split('/')) for b in data.get('badges')],
                    color=QtGui.QColor(data.get('color')),
                    display_name=data.get('display-name'),
                    tmi_sent_ts=data.get('tmi-sent-ts'),
                    user_id=data.get('user-id'),
                    login=data.get('name')
                )
            
            return cls(state, **data)
        
        else:
            raise ValueError
