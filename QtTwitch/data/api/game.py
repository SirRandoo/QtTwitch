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
from PyQt5 import QtCore, QtGui


class Game:
    """A game on Twitch."""
    
    def __init__(self, **kwargs):
        self._box_art_template: str = kwargs.get("box_art_url")
        self._id: str = kwargs.get("id")
        self._name: str = kwargs.get("name")
    
    # Properties #
    @property
    def id(self) -> str:
        """The Twitch ID of the game."""
        return self._id
    
    @property
    def name(self) -> str:
        """The name of the game."""
        return self._name
    
    # Asset Methods #
    def box_art_url(self, width: int = None, height: int = None) -> QtCore.QUrl:
        """Returns the url to the box art for this game."""
        if width is None:
            width = 128
        
        if height is None:
            height = 256
        
        return QtCore.QUrl(self._box_art_template.format(width=width, height=height))
    
    def box_art(self, width: int = None, height: int = None) -> QtGui.QImage:
        """Returns a QImage of the box art."""
