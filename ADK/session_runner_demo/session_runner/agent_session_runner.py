# To run this script, use the command: python ./session_runner/agent_session_runner.py

# DEMO: SESSION with RUNNER with a SEQUENTIAL AGENT

from agent import code_pipeline_agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
import asyncio, uuid


# Agent Interaction
async def call_agent(agent, query):
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # --- Constants ---
    APP_NAME = "code_writing_app"
    USER_ID = "dev_user"
    SESSION_ID = str(uuid.uuid4())
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Session and Runner
    session_service = InMemorySessionService()
    session = await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    runner = Runner(agent=agent, app_name=APP_NAME, session_service=session_service)

    # Pass user query to hte agent
    content = types.Content(role='user', parts=[types.Part(text=query)])

    # Run the agent within the session context
    events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=content)
    for event in events:
        # print(event)
        if event.is_final_response():
            final_response = event.content.parts[0].text
            print("\n------------------------------------------------------------")
            print("Agent Response: ", final_response)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#--------------------------------------------
# Entry point for the script  
#--------------------------------------------
if __name__ == "__main__":
    asyncio.run(
        call_agent(
            agent=code_pipeline_agent,
            query="Write a Python function to calculate the factorial of a number." 
    ))

