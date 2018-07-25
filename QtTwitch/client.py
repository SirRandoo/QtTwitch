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
import random

from PyQt5 import QtCore

from .dataclasses.qmessage import QMessage
from .irc import IRC


class Client(QtCore.QObject):
    on_raw_message = QtCore.pyqtSignal(object)
    
    def __init__(self, **kwargs):
        # Super Class #
        super(Client, self).__init__(parent=kwargs.get("parent"))
        
        # "Internal" Attributes #
        self._irc_connection = IRC(kwargs.get("nick", "justinfan123"), kwargs.get("token", "foobar"), parent=self)
        
        # Internal Calls #
        self._irc_connection.on_message.connect(self.on_raw_message.emit)
    
    def disconnect(self):
        pass
    
    def login(self, login: str = None, token: str = None):
        """Sets the credentials for the IRC connection."""
        if login is None or token is None:
            login = "justinfan{}".format(str(random.randint(9999)))
            token = None
        
        self._irc_connection.set_credentials(login, token)
    
    def logout(self):
        pass
    
    def connect(self):
        """Connects to Twitch's IRC servers."""
        self._irc_connection.connect()
    
    def connect_and_login(self, login: str = None, token: str = None):
        """Connects to Twitch's IRC servers and logs in with
        the provided credentials."""
        self.login(login, token)
        self.connect()
    
    def join(self, channel: str):
        """Tells the IRC connection to join a channel."""
        self._irc_connection.set_channel(channel)
    
    def part(self):
        """Tells the IRC connection to leave the current channel."""
        self._irc_connection.set_channel(None)
