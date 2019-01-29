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
import dataclasses

from PyQt5 import QtCore

__all__ = ['Game']


@dataclasses.dataclass(frozen=True)
class Game:
    """A game on Twitch."""
    id: str
    name: str
    url: str
    
    # Asset Methods #
    def box_art_url(self, width: int = None, height: int = None) -> QtCore.QUrl:
        """Returns the url to the box art for this game."""
        return QtCore.QUrl(self.url.format(width=width or 128, height=height or 256))
