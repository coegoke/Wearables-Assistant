"""
Chat API endpoints
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatRequest, ChatResponse, Message
from app.services.agent_service import agent_service
from app.services.channel_service import channel_service
import uuid
from datetime import datetime

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/message", response_model=ChatResponse)
async def send_message(request: ChatRequest):
    """
    Send a message and get AI response
    
    Args:
        request: Chat request with message and channel_id
    
    Returns:
        ChatResponse with assistant message and tool calls
    """
    try:
        # Verify channel exists
        channel_service.get_channel(request.channel_id)
        
        # Add user message to channel
        user_message = Message(
            id=str(uuid.uuid4()),
            role="user",
            content=request.message,
            timestamp=datetime.now()
        )
        channel_service.add_message(request.channel_id, user_message)
        
        # Get agent response
        assistant_message, tool_calls = agent_service.chat(
            request.channel_id,
            request.message
        )
        
        # Add assistant message to channel
        channel_service.add_message(request.channel_id, assistant_message)
        
        return ChatResponse(
            message=assistant_message,
            tool_calls=tool_calls if tool_calls else None
        )
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/history/{channel_id}")
async def get_history(channel_id: str):
    """
    Get message history for a channel
    
    Args:
        channel_id: Channel ID
    
    Returns:
        List of messages
    """
    try:
        messages = channel_service.get_messages(channel_id)
        return {"channel_id": channel_id, "messages": messages}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/history/{channel_id}")
async def clear_history(channel_id: str):
    """
    Clear message history for a channel
    
    Args:
        channel_id: Channel ID
    
    Returns:
        Success message
    """
    try:
        channel_service.clear_messages(channel_id)
        agent_service.clear_conversation(channel_id)
        return {"message": "History cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
