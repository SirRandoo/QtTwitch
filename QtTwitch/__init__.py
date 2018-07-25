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
from . import dataclasses, errors
from .enums import BroadcasterTypes, UserTypes, StreamTypes
from .utils import AugmentedMethod
from .bases import AbstractClient
from .client import Client
