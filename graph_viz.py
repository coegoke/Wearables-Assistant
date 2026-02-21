"""Utility functions for graph visualization."""
import io
from PIL import Image


def get_graph_image(app):
    """
    Generate a PNG image of the LangGraph workflow.
    
    Args:
        app: The compiled LangGraph application
    
    Returns:
        PIL Image object of the graph
    """
    try:
        # Get the graph as a PNG
        png_data = app.get_graph().draw_mermaid_png()
        
        # Convert to PIL Image
        image = Image.open(io.BytesIO(png_data))
        return image
    except Exception as e:
        print(f"Error generating graph image: {e}")
        # Create a simple placeholder image
        img = Image.new('RGB', (400, 300), color='white')
        return img


def get_graph_mermaid(app):
    """
    Get the Mermaid diagram code for the graph.
    
    Args:
        app: The compiled LangGraph application
    
    Returns:
        String containing Mermaid diagram code
    """
    try:
        return app.get_graph().draw_mermaid()
    except Exception as e:
        return f"Error generating graph: {e}"
