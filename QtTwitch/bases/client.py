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
# File Date: 12/27/2017
import abc


class AbstractClient(abc.ABC):
    """The base class for creating Twitch clients."""
    
    @abc.abstractmethod
    def connect(self):
        """Initiates a connection to Twitch."""

    @abc.abstractmethod
    def disconnect(self):
        """Disconnects from Twitch.
        Subclasses should call `logout` before continuing
        disconnection logic."""
    
    @abc.abstractmethod
    def login(self, login: str=None, token: str=None):
        """Logs into Twitch with the given credentials.
        Both `login` and `token` should be passed to
        connect to a Twitch account.  Subclasses should
        handle anonymous login."""
    
    @abc.abstractmethod
    def logout(self):
        """Logs out of Twitch."""
