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
import time
import typing

__all__ = {"CachedMethod"}


class CachedMethod:
    """A descriptor class mostly used for ratelimiting
    Twitch API calls.  Callables decorated with this
    class allow the callable to be called once every
    5 minutes (configurable).  If the callable is called
    again during this cooldown period, the last returned
    value(s) will be returned again."""
    
    def __init__(self, cooldown: float=300):
        """
        :param cooldown: The amount in seconds
        a callable cannot be used for.  During
        this period, the last valid request will
        be returned.
        """
        
        self._last_use = 0
        self._cooldown = cooldown
        self._last_result = None
    
    def freeze(self):
        self._last_use = time.time()
    
    def thaw(self):
        self._last_use = 0

    def is_frozen(self) -> bool:
        return (self._last_use - time.time()) < self._cooldown
    
    def __call__(self, f: typing.Callable):
        def wrapper(*args, **kwargs):
            if not self.is_frozen():
                result = f(*args, **kwargs)
                self._last_result = result
                self.freeze()
                
                return result
            
            else:
                return self._last_result
        return wrapper
