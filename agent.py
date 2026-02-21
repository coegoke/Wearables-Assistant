"""LangGraph agent for wearables assistant chatbot."""
from typing import Annotated, TypedDict, Literal
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from tools import (
    get_daily_steps,
    get_sleep_data,
    get_heart_rate_data,
    get_activity_history,
    get_weekly_summary,
    get_device_info,
    search_data_by_date_range
)

# Load environment variables
load_dotenv()


# Define tools using LangChain's @tool decorator
@tool
def daily_steps_tool(date: str = None, days: int = 7) -> str:
    """Get daily step counts. Use 'date' for a specific date (YYYY-MM-DD) or 'days' to look back multiple days."""
    return get_daily_steps(date, days)


@tool
def sleep_data_tool(date: str = None, days: int = 7) -> str:
    """Get sleep data including total sleep, deep sleep, REM sleep, and sleep score. 
    Use 'date' for a specific date (YYYY-MM-DD) or 'days' to look back multiple days."""
    return get_sleep_data(date, days)


@tool
def heart_rate_tool(date: str = None) -> str:
    """Get heart rate data including resting, average, max, and min heart rates. 
    Use 'date' for a specific date (YYYY-MM-DD) or leave empty for today."""
    return get_heart_rate_data(date)


@tool
def activity_history_tool(days: int = 14, activity_type: str = None) -> str:
    """Get workout and activity history. Optionally filter by activity type (e.g., 'Running', 'Cycling', 'Swimming')."""
    return get_activity_history(days, activity_type)


@tool
def weekly_summary_tool() -> str:
    """Get a comprehensive weekly summary of all health and fitness metrics."""
    return get_weekly_summary()


@tool
def device_info_tool() -> str:
    """Get information about the user's wearable device and profile."""
    return get_device_info()


@tool
def date_range_search_tool(start_date: str, end_date: str, metric_type: str = "steps") -> str:
    """Search for data within a specific date range. 
    Args:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        metric_type: Type of data ('steps' or 'sleep')
    """
    return search_data_by_date_range(start_date, end_date, metric_type)


# Define the state
class AgentState(TypedDict):
    """State of the agent."""
    messages: Annotated[list, add_messages]


# Create the tools list
tools = [
    daily_steps_tool,
    sleep_data_tool,
    heart_rate_tool,
    activity_history_tool,
    weekly_summary_tool,
    device_info_tool,
    date_range_search_tool
]


def create_agent():
    """Create the LangGraph agent with tools."""
    
    # Initialize the LLM with tools (using Groq)
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    llm_with_tools = llm.bind_tools(tools)
    
    # System message
    system_message = SystemMessage(content="""You are a helpful AI assistant for wearables and health tracking data. 
You have access to a database containing the user's fitness and health metrics from their wearable device.

You can help users with:
- Daily step counts and activity levels
- Sleep quality and patterns
- Heart rate data and trends
- Workout and exercise history
- Weekly summaries of all metrics
- Device and profile information
- Custom date range queries

IMPORTANT INSTRUCTIONS:
- NEVER mention the names of tools, functions, or technical implementation details (like "activity_history_tool", "daily_steps_tool", etc.)
- When you need to check data, simply say you're checking or reviewing the data, not which tool you're using
- Be natural and conversational - users don't need to know the technical details of how you retrieve information
- Instead of "I'll use the activity_history_tool", say "Let me check your activity history" or "I'll review your recent activities"
- Instead of "using the sleep_data_tool", say "Let me look at your sleep data" or "Checking your sleep records"
- Focus on the information and insights, not the mechanics of how you obtain them

Be friendly, informative, and provide insights when relevant. When users ask vague questions, 
check the appropriate data or ask for clarification. Always format data clearly and highlight important trends.""")
    
    # Define the agent node
    def call_model(state: AgentState) -> AgentState:
        """Call the model with the current state."""
        messages = state["messages"]
        
        # Add system message if this is the first call
        if not any(isinstance(m, SystemMessage) for m in messages):
            messages = [system_message] + messages
        
        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}
    
    # Define the tool execution node
    def execute_tools(state: AgentState) -> AgentState:
        """Execute tools based on the model's tool calls."""
        messages = state["messages"]
        last_message = messages[-1]
        
        # Get tool calls from the last message
        tool_calls = getattr(last_message, "tool_calls", [])
        
        if not tool_calls:
            return {"messages": []}
        
        # Create a mapping of tool names to tool functions
        tool_map = {tool.name: tool for tool in tools}
        
        # Execute each tool call
        tool_messages = []
        for tool_call in tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            
            if tool_name in tool_map:
                tool_func = tool_map[tool_name]
                try:
                    result = tool_func.invoke(tool_args)
                    tool_messages.append({
                        "role": "tool",
                        "content": str(result),
                        "tool_call_id": tool_call["id"],
                        "name": tool_name
                    })
                except Exception as e:
                    tool_messages.append({
                        "role": "tool",
                        "content": f"Error executing tool: {str(e)}",
                        "tool_call_id": tool_call["id"],
                        "name": tool_name
                    })
        
        return {"messages": tool_messages}
    
    # Define routing logic
    def should_continue(state: AgentState) -> Literal["tools", "end"]:
        """Determine if we should continue to tools or end."""
        messages = state["messages"]
        last_message = messages[-1]
        
        # If there are tool calls, continue to tools
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "tools"
        
        # Otherwise, end
        return "end"
    
    # Build the graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", execute_tools)
    
    # Set entry point
    workflow.set_entry_point("agent")
    
    # Add edges
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "end": END
        }
    )
    workflow.add_edge("tools", "agent")
    
    # Compile the graph
    app = workflow.compile()
    
    return app


def chat(agent, user_message: str, conversation_history: list = None) -> tuple[str, list]:
    """
    Send a message to the agent and get a response.
    
    Args:
        agent: The compiled LangGraph agent
        user_message: The user's message
        conversation_history: Previous messages in the conversation
    
    Returns:
        Tuple of (response text, updated conversation history)
    """
    if conversation_history is None:
        conversation_history = []
    
    # Add the user message
    conversation_history.append(HumanMessage(content=user_message))
    
    # Run the agent
    result = agent.invoke({"messages": conversation_history})
    
    # Get the final response
    final_message = result["messages"][-1]
    response_text = final_message.content
    
    # Update conversation history
    conversation_history = result["messages"]
    
    return response_text, conversation_history
