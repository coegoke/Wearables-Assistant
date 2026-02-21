"""
Agent service - manages LangGraph agent and conversations
"""
import uuid
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import sys
import os

# Add parent directory to path to import existing modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from agent import create_agent, chat as agent_chat
from app.models.schemas import Message, ToolCall


class AgentService:
    """Service for managing agent conversations"""
    
    def __init__(self):
        self.agent = None
        self.conversation_histories: Dict[str, list] = {}  # channel_id -> conversation history
        self.initialize_agent()
    
    def initialize_agent(self):
        """Initialize the LangGraph agent"""
        try:
            self.agent = create_agent()
            return True
        except Exception as e:
            print(f"Error initializing agent: {e}")
            return False
    
    def is_initialized(self) -> bool:
        """Check if agent is initialized"""
        return self.agent is not None
    
    def get_or_create_conversation(self, channel_id: str) -> list:
        """Get or create conversation history for a channel"""
        if channel_id not in self.conversation_histories:
            self.conversation_histories[channel_id] = []
        return self.conversation_histories[channel_id]
    
    def extract_tool_calls(self, messages: list) -> List[ToolCall]:
        """Extract tool calls from LangChain messages"""
        tool_calls = []
        
        for msg in messages:
            # Check for tool calls in the message
            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                for tool_call in msg.tool_calls:
                    tool_calls.append(ToolCall(
                        tool_name=tool_call.get('name', 'Unknown'),
                        arguments=tool_call.get('args', {}),
                        result=None
                    ))
            
            # Check for tool results
            if hasattr(msg, 'type') and msg.type == 'tool':
                # Find corresponding tool call and add result
                if tool_calls and hasattr(msg, 'name'):
                    for tc in tool_calls:
                        if tc.tool_name == msg.name and tc.result is None:
                            tc.result = msg.content[:500]  # Limit result length
                            break
        
        return tool_calls
    
    def chat(self, channel_id: str, user_message: str) -> Tuple[Message, List[ToolCall]]:
        """
        Process user message and return response
        
        Args:
            channel_id: Channel ID
            user_message: User's message
        
        Returns:
            Tuple of (assistant message, tool calls)
        """
        if not self.is_initialized():
            raise RuntimeError("Agent not initialized")
        
        # Get conversation history for this channel
        conversation_history = self.get_or_create_conversation(channel_id)
        
        # Call agent
        response_text, updated_history = agent_chat(
            self.agent,
            user_message,
            conversation_history
        )
        
        # Update stored history
        self.conversation_histories[channel_id] = updated_history
        
        # Extract tool calls
        tool_calls = self.extract_tool_calls(updated_history)
        
        # Create response message
        response_message = Message(
            id=str(uuid.uuid4()),
            role="assistant",
            content=response_text,
            timestamp=datetime.now(),
            tool_calls=tool_calls if tool_calls else None
        )
        
        return response_message, tool_calls
    
    def clear_conversation(self, channel_id: str):
        """Clear conversation history for a channel"""
        if channel_id in self.conversation_histories:
            self.conversation_histories[channel_id] = []
    
    def get_conversation_count(self, channel_id: str) -> int:
        """Get message count for a channel"""
        if channel_id in self.conversation_histories:
            return len(self.conversation_histories[channel_id])
        return 0


# Global agent service instance
agent_service = AgentService()
