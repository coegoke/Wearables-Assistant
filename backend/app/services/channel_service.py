"""
Channel service - manages chat channels
"""
import uuid
from typing import Dict, List
from datetime import datetime
from app.models.schemas import Channel, Message


class ChannelService:
    """Service for managing chat channels"""
    
    def __init__(self):
        self.channels: Dict[str, Channel] = {}
        self.channel_messages: Dict[str, List[Message]] = {}
        
        # Create default channel
        self.create_channel("General")
    
    def create_channel(self, name: str) -> Channel:
        """Create a new channel"""
        channel_id = str(uuid.uuid4())
        channel = Channel(
            id=channel_id,
            name=name,
            created_at=datetime.now(),
            message_count=0
        )
        self.channels[channel_id] = channel
        self.channel_messages[channel_id] = []
        return channel
    
    def get_channel(self, channel_id: str) -> Channel:
        """Get channel by ID"""
        if channel_id not in self.channels:
            raise ValueError(f"Channel {channel_id} not found")
        return self.channels[channel_id]
    
    def list_channels(self) -> List[Channel]:
        """List all channels"""
        return list(self.channels.values())
    
    def delete_channel(self, channel_id: str) -> bool:
        """Delete a channel"""
        if channel_id in self.channels:
            del self.channels[channel_id]
            if channel_id in self.channel_messages:
                del self.channel_messages[channel_id]
            return True
        return False
    
    def add_message(self, channel_id: str, message: Message):
        """Add message to channel"""
        if channel_id not in self.channels:
            raise ValueError(f"Channel {channel_id} not found")
        
        if channel_id not in self.channel_messages:
            self.channel_messages[channel_id] = []
        
        self.channel_messages[channel_id].append(message)
        self.channels[channel_id].message_count += 1
    
    def get_messages(self, channel_id: str) -> List[Message]:
        """Get all messages in a channel"""
        if channel_id not in self.channels:
            raise ValueError(f"Channel {channel_id} not found")
        
        return self.channel_messages.get(channel_id, [])
    
    def clear_messages(self, channel_id: str):
        """Clear all messages in a channel"""
        if channel_id in self.channel_messages:
            self.channel_messages[channel_id] = []
            self.channels[channel_id].message_count = 0


# Global channel service instance
channel_service = ChannelService()
