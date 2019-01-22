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
import typing

from PyQt5 import QtCore, QtGui


class Cheermote:
    """A cheermote."""
    
    def __init__(self, state, **kwargs):
        # "Private" Attributes #
        self._state = state
        
        self._prefix: str = kwargs.get("prefix")
        self._minimum_amount: int = kwargs.get("min_amount")
        self._scales: typing.List[str] = list()
        self._color: QtGui.QColor = kwargs.get("color")
        self._id: str = kwargs.get("id")
        self._images: dict = kwargs.get("images")
        self._amount: int = kwargs.get("amount", self._minimum_amount)
        self._can_cheer: bool = kwargs.get("can_cheer")
        self._priority: int = kwargs.get("priority")
        self._backgrounds: typing.List[str] = kwargs.get("backgrounds")
        self._states: typing.List[str] = kwargs.get("states")
        self._type: str = kwargs.get("type")
        self._updated_at: datetime.datetime = kwargs.get("updated_at")
    
    # Property #
    @property
    def amount(self) -> int:
        """The amount of bits this cheermote was cheered with."""
        return self._amount
    
    @amount.setter
    def amount(self, value: int):
        self._amount = value
    
    @property
    def prefix(self) -> str:
        """The prefix of this cheermote."""
        return self._prefix
    
    @property
    def id(self) -> str:
        """The Twitch ID of this cheermote."""
        return self._id
    
    @property
    def scales(self) -> typing.List[str]:
        """The scales this cheermote supports."""
        return self._scales.copy()
    
    @property
    def color(self) -> QtGui.QColor:
        """The hex color of this cheermote."""
        return self._color
    
    @property
    def min_amount(self) -> int:
        """The minimum amount of bits that must be cheered before this
        cheermote should be displayed."""
        return self._minimum_amount
    
    @property
    def can_cheer(self) -> bool:
        """Whether or not this cheermote can be cheered."""
        return self._can_cheer
    
    @property
    def priority(self) -> int:
        """The priority this cheermote has compared to other cheermotes."""
        return self._priority
    
    @property
    def backgrounds(self) -> typing.List[str]:
        """The different backgrounds this cheermote supports."""
        return self._backgrounds
    
    @property
    def states(self) -> typing.List[str]:
        """The different states this cheermote supports."""
        return self._states
    
    @property
    def type(self) -> str:
        """The type of cheermote this is."""
        return self._type
    
    @property
    def updated_at(self) -> datetime.datetime:
        """The last time this cheermote was updated at."""
        return self._updated_at
    
    # Asset Methods #
    def static_url(self, theme: str, scale: str) -> QtCore.QUrl:
        """Returns a QUrl of the static cheermote at `scale` in `theme`."""
        if theme in self._images:
            themed: dict = self._images.get(theme)
            
            if "static" in themed:
                static_themed: dict = themed.get("static")
                
                if scale in static_themed:
                    return QtCore.QUrl(static_themed.get(scale))
                
                else:
                    raise KeyError(f'Cheermote does not support specified scale "{scale}"!')
            
            else:
                raise KeyError('Does not support static cheermotes!')
        
        else:
            raise KeyError(f'Cheermote does not support specified theme "{theme}"!')
    
    def animated_url(self, theme: str, scale: str) -> QtCore.QUrl:
        """Returns a QUrl of the animated cheermote at `scale` in `theme`."""
        if theme in self._images:
            themed: dict = self._images.get(theme)
            
            if "animated" in themed:
                animated_themed: dict = themed.get("animated")
                
                if scale in animated_themed:
                    return QtCore.QUrl(animated_themed.get(scale))
                
                else:
                    raise KeyError(f'Cheermote does not support specified scale "{scale}"!')
            
            else:
                raise KeyError('Does not support animated cheermotes!')
        
        else:
            raise KeyError(f'Cheermote does not support specified theme "{theme}"!')
    
    def static(self, theme: str, scale: str) -> QtGui.QImage:
        """Returns a QImage of the cheermote with `theme` at `scale`."""
        if theme in self._images:
            themed: dict = self._images.get(theme)
            
            if "static" in themed:
                static_themed: dict = themed.get("static")
                
                if scale in static_themed:
                    pass  # TODO: Fetch the image
                
                else:
                    raise KeyError(f'Cheermote does not support specified scale "{scale}"')
            
            else:
                raise KeyError('Does not support static cheermotes!')
        
        else:
            raise KeyError(f'Cheermote does not support specified theme "{theme}"!')
    
    def animated(self, theme: str, scale: str) -> QtGui.QImage:
        """Returns a QImage of the cheermote with `theme` at `scale`."""
        if theme in self._images:
            themed: dict = self._images.get(theme)
            
            if "animated" in themed:
                animated_themed: dict = themed.get("animated")
                
                if scale in animated_themed:
                    pass  # TODO: Fetch GIF
                
                else:
                    raise KeyError(f'Cheermote does not support specified scale "{scale}"')
            
            else:
                raise KeyError('Does not support static cheermotes!')
        
        else:
            raise KeyError(f'Cheermote does not support specified theme "{theme}"!')
    
    # Magic Methods #
    def __str__(self):
        return f'{self._prefix}{self.amount}'
