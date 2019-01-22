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
import re
import typing

from ...enums import irc


@dataclasses.dataclass(frozen=True)
class SystemMessage:
    """A basic dataclass for system messages."""
    type: irc.SysMsgTypes
    user: str
    message: str
    response_code: typing.Optional[irc.IrcResponses]
    host: str = 'tmi.twitch.tv'


@dataclasses.dataclass(frozen=True)
class PingMessage(SystemMessage):
    """A system message for IRC pings."""


class SystemMessage:
    """A system message from Twitch."""
    
    SYSTEM = re.compile(':tmi\.twitch\.tv (?P<response>\d+) (?P<user>\w+) :(?P<message>.*)')
