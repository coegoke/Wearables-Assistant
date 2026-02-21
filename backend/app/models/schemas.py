"""
Pydantic models for request/response schemas
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


class MessageBase(BaseModel):
    """Base message model"""
    role: str = Field(..., description="Message role: user or assistant")
    content: str = Field(..., description="Message content")


class ToolCall(BaseModel):
    """Tool call information"""
    tool_name: str = Field(..., description="Name of the tool called")
    arguments: Dict[str, Any] = Field(default_factory=dict, description="Tool arguments")
    result: Optional[str] = Field(None, description="Tool execution result")


class Message(MessageBase):
    """Complete message model with metadata"""
    id: str = Field(..., description="Message unique ID")
    timestamp: datetime = Field(default_factory=datetime.now, description="Message timestamp")
    tool_calls: Optional[List[ToolCall]] = Field(None, description="Tool calls if any")


class ChatRequest(BaseModel):
    """Chat message request"""
    message: str = Field(..., description="User message")
    channel_id: str = Field(..., description="Channel ID")


class ChatResponse(BaseModel):
    """Chat message response"""
    message: Message = Field(..., description="Assistant response message")
    tool_calls: Optional[List[ToolCall]] = Field(None, description="Tool calls made")


class Channel(BaseModel):
    """Channel model"""
    id: str = Field(..., description="Channel unique ID")
    name: str = Field(..., description="Channel name")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    message_count: int = Field(default=0, description="Number of messages in channel")


class ChannelCreate(BaseModel):
    """Channel creation request"""
    name: str = Field(..., description="Channel name", min_length=1, max_length=100)


class ChannelList(BaseModel):
    """List of channels"""
    channels: List[Channel] = Field(..., description="List of channels")


class MessageHistory(BaseModel):
    """Channel message history"""
    channel_id: str = Field(..., description="Channel ID")
    messages: List[Message] = Field(..., description="List of messages")


class GraphResponse(BaseModel):
    """Graph visualization response"""
    mermaid: str = Field(..., description="Mermaid diagram code")
    png_base64: Optional[str] = Field(None, description="PNG image as base64")


class HealthCheck(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(default_factory=datetime.now, description="Check timestamp")
    agent_initialized: bool = Field(..., description="Whether agent is initialized")
