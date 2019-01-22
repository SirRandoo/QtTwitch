# This file is part of QtTwitch.
#
# QtTwitch is free software:
# you can redistribute it and/or
# modify it under the terms of the
# GNU General Public License as
# published by the Free Software
# Foundation, either version 3 of
# the License, or (at your option)
# any later version.
#
# QtTwitch is distributed in the hope
# that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License
# for more details.
#
# You should have received a copy of
# the GNU General Public License along
# with QtTwitch.
# If not, see <http://www.gnu.org/licenses/>.
# TODO: Fix Client

from PyQt5 import QtCore

from .irc import ManagedConnection


class Client(QtCore.QObject):
    """A client for connecting to Twitch's servers."""
    on_message = QtCore.pyqtSignal()
    
    def __init__(self, **kwargs):
        # Super Call #
        super(Client, self).__init__(parent=kwargs.get("parent"))
    
        # "Private" Attributes #
        self._irc = ManagedConnection(username=kwargs.get("username"), token=kwargs.get("token"), parent=self)
        
        # Internal Calls #
        self._irc.on_message.connect(self.on_message)
    
        # Aliases #
        self.connect = self._irc.connect
        self.disconnect = self._irc.disconnect
        self.join = self._irc.join
        self.part = self._irc.part
    
        self.qdisconnect = super(Client, self).disconnect
