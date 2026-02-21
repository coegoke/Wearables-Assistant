"""
Channel API endpoints
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import Channel, ChannelCreate, ChannelList
from app.services.channel_service import channel_service

router = APIRouter(prefix="/channels", tags=["channels"])


@router.post("/", response_model=Channel)
async def create_channel(request: ChannelCreate):
    """
    Create a new channel
    
    Args:
        request: Channel creation request with name
    
    Returns:
        Created channel
    """
    try:
        channel = channel_service.create_channel(request.name)
        return channel
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=ChannelList)
async def list_channels():
    """
    List all channels
    
    Returns:
        List of all channels
    """
    channels = channel_service.list_channels()
    return ChannelList(channels=channels)


@router.get("/{channel_id}", response_model=Channel)
async def get_channel(channel_id: str):
    """
    Get channel by ID
    
    Args:
        channel_id: Channel ID
    
    Returns:
        Channel details
    """
    try:
        channel = channel_service.get_channel(channel_id)
        return channel
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{channel_id}")
async def delete_channel(channel_id: str):
    """
    Delete a channel
    
    Args:
        channel_id: Channel ID
    
    Returns:
        Success message
    """
    success = channel_service.delete_channel(channel_id)
    if not success:
        raise HTTPException(status_code=404, detail="Channel not found")
    return {"message": "Channel deleted successfully"}
