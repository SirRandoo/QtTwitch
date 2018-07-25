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
# File Date: 11/14/2017
# TODO: Move user-specific data to QUser
# TODO: Make `author` return a QUser
from PyQt5 import QtCore


class QMessage(QtCore.QObject):
    """Represents a message from Twitch."""
    
    @property
    def content(self):
        return getattr(self, "_mContent")
    
    @property
    def author(self):
        return getattr(self, "_mAuthor")
    
    def is_mod(self) -> bool:
        """Returns whether or not the message was sent by a moderator."""
        tags = getattr(self, "_mTags", dict())
        
        return tags.get("mod", False)
    
    def is_sub(self) -> bool:
        """Returns whether or not the messages was sent by a subscriber."""
        tags = getattr(self, "_mTags", dict())
        
        return tags.get("subscriber", False)
    
    def color_hex(self) -> str:
        """Returns the message's author's color.  Returns None if the author
        next set a color."""
        tags = getattr(self, "_mTags", dict())
        
        return tags.get("color", None)
    
    @classmethod
    def from_match(cls, match_dict: dict) -> 'QMessage':
        """Converts a re.match message dict into a QMessage."""
        message = cls.__new__(cls)
        message._mAuthor = match_dict.get("name")
        message._mChannel = match_dict.get("channel")
        message._mContent = match_dict.get("message")
        message._mTags = dict()
        
        for tag_segment in match_dict.get("tags", "").split(";"):
            tag_name, tag_value = tag_segment.split("=", 1)  # type: str, str
            
            if tag_name == "badges":
                message._mTags[tag_name] = dict()
                
                if tag_value:
                    for badge_segment in tag_value.split(","):
                        badge_name, badge_version = badge_segment.split("/")
                        
                        message._mTags[tag_name][badge_name] = badge_version

            elif tag_name == "emotes":
                message._mTags[tag_name] = dict()
                
                if tag_value:
                    for emote_segment in tag_value.split("/"):
                        emote_id, emote_ranges = emote_segment.split(":")
                        message._mTags[tag_name][emote_id] = list()
            
                        for range_segment in emote_ranges.split(","):
                            start, end = range_segment.split("-")
                
                            message._mTags[tag_name][emote_id].append((int(start), int(end)))
            
            elif tag_name in ["display-name", "id", "room-id", "user-id", "user-type"]:
                message._mTags[tag_name] = tag_value
            
            elif tag_name in ["mod", "subscriber", "turbo"]:
                message._mTags[tag_name] = bool(int(tag_value))
            
            elif tag_name == "bits":
                message._mTags[tag_name] = int(tag_value)
            
            elif tag_name == "color":
                message._mTags[tag_name] = tag_value.lstrip("#")
        
        return message
