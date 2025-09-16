
# DEMO: Tool Use + Callback

from google.adk.agents import Agent
from google.adk.tools import ToolContext
from google.adk.tools.base_tool import BaseTool
from typing import Dict, Any, Optional

from dotenv import load_dotenv
load_dotenv()

# Tool - Set/update preference
def update_user_preference(preference: str, value: str, tool_context: ToolContext):
    # Get current preferences or initialize if none exist
    if 'preferences' not in tool_context.state:
        tool_context.state.preferences = {}

    # Write the updated dictionary back to the state
    tool_context.state.preferences[preference] = value

    # print(tool_context.state.preferences[preference])
    print(f"Tool: Updated user preference '{preference}' to '{value}'")

    return {"Status": "success", "updated_preference": preference}

# Callback: Get/retrieve preference
def retrieve_user_preference(tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext, tool_response: Dict) -> Optional[Dict]:

    # if 'preferences' not in tool_context.state:
    #     raise ValueError("No preferences found in state.")
    #     return {"Status": "error", "message": "No preferences found."}

    print(f"Tool: Retrieved user preferences: {tool_context.state.preferences}")
    return None
  

# Agent
my_agent = Agent(
    name='main_agent',
    instruction="""You are a helpful agent. Answer general queries. 
    If the user provides preference to be set, use the 'update_user_preference' tool.
    """,
    model='gemini-2.0-flash',
    tools=[update_user_preference],
    after_tool_callback= retrieve_user_preference
    )

# When the LLM calls update_user_preference(preference='theme', value='dark', ...):
# The tool_context.state will be updated, and the change will be part of the
# resulting tool response event's actions.state_delta.

root_agent=my_agent