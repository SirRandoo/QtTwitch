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
import logging
import re
import typing

from ...enums import irc

__all__ = ['SystemMessage', 'PingMessage']

# Regex
system_message = re.compile(':tmi\.twitch\.tv (?P<code>\d{3}) (?P<user>\w{4,25}) :(?P<message>.*)')
system_alt = re.compile('@(?P<tags>.*) :tmi\.twitch\.tv (?P<type>\w+) #(?P<channel>\w{4,25}) :(?P<message>.*)')


@dataclasses.dataclass(frozen=True)
class SystemMessage:
    """A basic dataclass for system messages."""
    type: irc.SysMsgTypes
    user: str
    message: str
    response_code: typing.Optional[irc.IrcResponses]
    host: str = 'tmi.twitch.tv'

    @classmethod
    def from_string(cls, string: str) -> 'SystemMessage':
        """Transforms a string into a SystemMessage."""
        if string.startswith('PING'):  # We'll assume it's a PING message.
            return PingMessage()
    
        elif string.startswith(':'):  # This is a system message from Twitch.
            match = system_message.match(string)
        
            if match:
                match_dict = match.groupdict()
            
                try:
                    code = irc.IrcResponses(match_dict.get('code'))
            
                except ValueError:
                    logging.getLogger(__name__).warning(f'Unsupported response code #{match_dict.get("code")}!')
                    code = None
            
                return SystemMessage(
                    user='twitch.tv',
                    message=match_dict.get('message'),
                    type=irc.SysMsgTypes.GENERIC,
                    response_code=code
                )
    
        elif string.startswith('@'):
            match = system_alt.match(string)
        
            if match:
                match_dict = match.groupdict()
    
        else:
            raise ValueError(f'Unsupported string "{string}"!')


@dataclasses.dataclass(frozen=True)
class PingMessage(SystemMessage):
    """A system message for IRC pings."""
    type: irc.SysMsgTypes = irc.SysMsgTypes.PING
    user: str = 'twitch.tv'
    message: str = 'ping'


class SystemMessage:
    """A system message from Twitch."""
    
    SYSTEM = re.compile(':tmi\.twitch\.tv (?P<response>\d+) (?P<user>\w+) :(?P<message>.*)')
