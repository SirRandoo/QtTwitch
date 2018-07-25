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
# File Date: 11/15/2017
from PyQt5 import QtCore
from ..enums import UserTypes, BroadcasterTypes
from ..utils import AugmentedMethod


class QUser(QtCore.QObject):
    """Represents a Twitch user."""
    
    def __init__(self, data: dict, state, *, parent: QtCore.QObject=None):
        # Super Call #
        super(QUser, self).__init__(parent=parent)
        
        # Attributes #
        self.state = state
        self.id = None  # type: str
        self.username = None  # type: str
        self.display_name = None  # type: str
        self.type = None  # type: UserTypes
        
        # Internal Calls #
        self._patch(data)
    
    def _patch(self, data: dict):
        self.id = data.pop("id")
        self.username = data.pop("login")
        self.display_name = data.get("display_name", self.username.title())
        self.type = UserTypes(data.pop("type", ""))
        self.broadcaster_type = BroadcasterTypes(data.pop("broadcaster_type", ""))
        self.description = data.get("description")
        self.profile_image_url = data.get("profile_image_url")
        self.offline_image_url = data.get("offline_image_url")
        self.view_count = data.get("view_count", 0)
        self.email = data.get("email")
    
    @AugmentedMethod()
    def update(self):
        url = self.state.stitch("helix", "users", id=self.id)
        
        try:
            self._patch(self.state.get(url).json())
        
        except ValueError:
            pass
