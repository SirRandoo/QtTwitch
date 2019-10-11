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
import datetime

from PyQt5 import QtCore, QtGui

from .game import Game
from .user import User


class Stream(QtCore.QObject):
    """A channel on Twitch."""
    
    def __init__(self, **kwargs):
        # Super Call #
        super(Stream, self).__init__(parent=kwargs.get("parent"))
        
        # "Private" Attributes #
        self._id: str = kwargs.pop("id")
        self._game: Game = kwargs.get("game")
        self._language: str = kwargs.get("language")
        self._started_at: datetime.datetime = kwargs.get("started_at")
        self._thumbnail_url: str = kwargs.get("thumbnail_url")
        self._title: str = kwargs.get("title")
        self._type: str = kwargs.get("type")
        self._broadcaster: User = kwargs.get("broadcaster")
        self._viewer_count: int = kwargs.get("viewer_count")
        
        # "Public" Attributes #
    
    # Properties #
    @property
    def game(self) -> Game:
        """The current game the streamer is playing."""
        return self._game
    
    @property
    def id(self) -> str:
        """The Twitch ID of the stream."""
        return self._id
    
    @property
    def language(self) -> str:
        """The primary language of the stream."""
        return self._language
    
    @property
    def started_at(self) -> datetime.datetime:
        """A datetime object representing when this stream was started."""
        return self._started_at
    
    @property
    def title(self) -> str:
        """The title of the stream."""
        return self._title
    
    @property
    def broadcaster(self) -> User:
        """The broadcaster of this stream."""
        return self._broadcaster
    
    @property
    def viewer_count(self) -> int:
        """The number of viewers watching the stream."""
        return self._viewer_count
    
    # Asset Methods #
    def thumbnail_url(self, width: int = None, height: int = None) -> QtCore.QUrl:
        """The url of the stream's thumbnail."""
        if width is None:
            width = 800
        
        if height is None:
            height = 600
        
        return QtCore.QUrl(self._thumbnail_url.format(width=width, height=height))
    
    def thumbnail(self, width: int = None, height: int = None) -> QtGui.QImage:
        """Returns a QImage of the stream's thumbnail."""
