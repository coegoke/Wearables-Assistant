"""
Graph visualization API endpoints
"""
from fastapi import APIRouter
from app.models.schemas import GraphResponse
from app.services.graph_service import graph_service

router = APIRouter(prefix="/graph", tags=["graph"])


@router.get("/", response_model=GraphResponse)
async def get_graph():
    """
    Get LangGraph workflow visualization
    
    Returns:
        Graph visualization as Mermaid diagram and optional PNG
    """
    return graph_service.get_graph()
