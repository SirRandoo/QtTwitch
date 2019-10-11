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
import logging
import typing

from PyQt5 import QtCore

from . import dataclasses as dataklasses
from .gateway import Gateway
from .http import Http
from .parser import Parser

__all__ = ['Client']

logger = logging.getLogger(__name__)


class Client(QtCore.QObject):
    """A client for connecting to Twitch's servers."""
    # Signals
    on_message = QtCore.pyqtSignal(object)
    
    def __init__(self, **kwargs):
        """
        :param username: The username to use for authenticating to Twitch's IRC
                         servers.  If no username is provided, the client will
                         log in anonymously.
        :param token: The OAuth token to use for authenticating to Twitch's IRC
                      servers, and authenticated api requests.  If no token is
                      provided, the client will log in anonymously, and
                      authenticated requests will fail.
        :param client_id: The client id to use for api requests.  If no client
                          id is provided, api requests will probably fail.
        :param factory: A QRequestFactory to use for api requests.  If one is
                        not provided, a new one will be created.
        :param parent: A QObject to act as this object's parent.  If no parent
                       is provided, the client will have to be manually disposed
                       of.
        """
    
        # Super call
        super(Client, self).__init__(parent=kwargs.get('parent'))
    
        # Public attributes
        self.irc = Gateway(username=kwargs.get('username'), token=kwargs.get('token'), parent=self)
        self.http = Http(client_id=kwargs.get('client_id'), token=kwargs.get('token'), factory=kwargs.get('factory'))
        self.parser = Parser(self)
    
        self.channels: typing.List[dataklasses.Channel] = []
        self.emotes: typing.Dict[str, typing.List[dataklasses.Emote]] = {}  # id: [emote, emote, ...]
    
        # Internal calls
        self.stitch_signals()
    
    # Internal methods
    def stitch_signals(self):
        """Stitches the QObject signals to their respective slots."""
        # Irc gateway signals
        self.irc.on_message.connect(self.parse_message)
    
    # Message methods
    def parse_message(self, message: str):
        """Parses a raw IRC message."""
        try:
            message = self._parser.parse(message)
        
        except (ValueError, KeyError) as e:
            logger.warning(f'Could not parse message "{message}"!  ({e.__class__.__name__}({e!s}))')
        
        else:
            self.on_message.emit(message)
