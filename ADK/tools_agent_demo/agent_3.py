# DEMO: Controlling Agent Flow
# The tool_context.actions attribute holds an EventActions object.
# Modifying attributes on this object allows your tool to influence 
# what the agent or framework does after the tool finishes execution.

# Run the code:
# python  .\tools_agent_demo\agent.py


"""
This example illustrates how a tool, 
through EventActions in its ToolContext, 
can dynamically influence the flow of the conversation 
by transferring control to another specialized agent.
"""
"""
Explanation:
We define two agents: main_agent and support_agent. 
The main_agent is designed to be the initial point of contact.
The check_and_transfer tool, when called by main_agent, examines the user's query.
If the query contains the word "urgent", the tool accesses the tool_context, 
specifically tool_context.actions, and sets the transfer_to_agent attribute to support_agent.
This action signals to the framework to transfer the control of the conversation 
to the agent named support_agent.
When the main_agent processes the urgent query, 
the check_and_transfer tool triggers the transfer. 
The subsequent response would ideally come from the support_agent.
For a normal query without urgency, the tool simply processes it 
without triggering a transfer.
"""



from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import ToolContext
from google.genai import types
import asyncio

from dotenv import load_dotenv
load_dotenv()

APP_NAME="customer_support_agent"
USER_ID="user1234"
SESSION_ID="1234"


def check_and_transfer(query: str, tool_context: ToolContext) -> str:
    """Checks if the query requires escalation and transfers to another agent if needed."""
    if "urgent" in query.lower():
        print("Tool: Detected urgency, transferring to the support agent.")
        tool_context.actions.transfer_to_agent = "support_agent"
        return "Transferring to the support agent..."
    else:
        return f"Processed query: '{query}'. No further action needed."

escalation_tool = FunctionTool(func=check_and_transfer)

main_agent = Agent(
    model='gemini-2.0-flash',
    name='main_agent',
    instruction="""You are the first point of contact for customer support of an analytics tool. Answer general queries. If the user indicates urgency, use the 'check_and_transfer' tool.""",
    tools=[check_and_transfer]
)

support_agent = Agent(
    model='gemini-2.0-flash',
    name='support_agent',
    instruction="""You are the dedicated support agent. Mentioned you are a support handler and please help the user with their urgent issue."""
)

main_agent.sub_agents = [support_agent]

# Session and Runner
async def setup_session_and_runner():
    session_service = InMemorySessionService()
    session = await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    runner = Runner(agent=main_agent, app_name=APP_NAME, session_service=session_service)
    return session, runner

# Agent Interaction
async def call_agent_async(query):
    content = types.Content(role='user', parts=[types.Part(text=query)])
    session, runner = await setup_session_and_runner()
    events = runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content)

    async for event in events:
        if event.is_final_response():
            final_response = event.content.parts[0].text
            print("Agent Response: ", final_response)

# Note: In Colab, you can directly use 'await' at the top level.
# If running this code as a standalone Python script, you'll need to use asyncio.run() or manage the event loop.
# asyncio.run(call_agent_async("this is urgent, i can not login"))
asyncio.run(call_agent_async("Who is Mahatma Gandhi?"))

