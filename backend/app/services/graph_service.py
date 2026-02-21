"""
Graph service - manages graph visualization
"""
import sys
import os
import base64
import io

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from graph_viz import get_graph_mermaid
from app.services.agent_service import agent_service
from app.models.schemas import GraphResponse


class GraphService:
    """Service for graph visualization"""
    
    def get_graph(self) -> GraphResponse:
        """Get graph visualization"""
        if not agent_service.is_initialized():
            return GraphResponse(
                mermaid="graph TD\n  A[Agent Not Initialized]",
                png_base64=None
            )
        
        try:
            # Get mermaid diagram
            mermaid = get_graph_mermaid(agent_service.agent)
            
            # Try to get PNG as base64
            png_base64 = None
            try:
                from graph_viz import get_graph_image
                img = get_graph_image(agent_service.agent)
                if img:
                    buffered = io.BytesIO()
                    img.save(buffered, format="PNG")
                    png_base64 = base64.b64encode(buffered.getvalue()).decode()
            except Exception as e:
                print(f"Could not generate PNG: {e}")
            
            return GraphResponse(
                mermaid=mermaid,
                png_base64=png_base64
            )
        
        except Exception as e:
            print(f"Error generating graph: {e}")
            return GraphResponse(
                mermaid=f"graph TD\n  A[Error: {str(e)}]",
                png_base64=None
            )


# Global graph service instance
graph_service = GraphService()
