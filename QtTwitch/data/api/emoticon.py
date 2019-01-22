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
from PyQt5 import QtCore


class Emoticon(QtCore.QObject):
    """Represents an emoticon from Twitch."""
    
    def __init__(self, state, **kwargs):
        # Super Call #
        super(Emoticon, self).__init__(parent=kwargs.get('parent'))
        
        # "Private" Attributes #
        self._state = state
        
        self._id: str = kwargs.pop('id')
        self._code: str = kwargs.pop('code')
        self._set: str = kwargs.get('emote_set')
