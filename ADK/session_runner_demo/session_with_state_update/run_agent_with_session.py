# To run this script, use the command: python .\session_runner_demo\session_with_state_update\run_agent_with_session.py
# Session with State Update

import asyncio
import uuid, time

from post_agent import root_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from google.adk.events import Event, EventActions

async def main():
    # Define session service
    session_service = InMemorySessionService()

    # Define state context for the session
    # This context will be attached to the session and be available to the agent during its execution
    state_context = {
        "user": "Soharab",
        "preference": "Paragraph containing exactly 3 sentences (each starting with a `#` symbol) about the given topic in the style of the individual mentioned",
        # "style": "Ernest Hemingway",
        # "style": "William Shakespeare",
        "style": "Rabindranath Tagore",
        "response": "Reponse of the agent will be populated here after the agent runs",
    }
    
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    SESSION_ID = str(uuid.uuid4())
    USER_ID = "soharab"
    APP_NAME = "PostGenerator"

    # Create a new session inside session_service which is of type InMemorySessionService
    # Await the coroutine to get the session object
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
        state=state_context, #<== Pass the state context to session object
    )

    print("Session ID:", session.id) # Note this is `id` not `session_id`
    print("Session App Name:", session.app_name)
    print("Session User ID:", session.user_id)
    print("Session State Before the Agent Runs:\n", session.state)

    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Create a Runner instance
    runner = Runner(
        agent=root_agent, #<= Assign the agent to runner
        session_service=session_service,
        app_name=APP_NAME,
    )

    user_query = types.Content(
        role="user",
        parts=[
            types.Part(
                text="What is socialism?",
            )
        ],
    )
      
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Run the agent with session and user query   
    # runner.run() coroutine
    for event in runner.run(
            user_id=USER_ID,
            session_id=SESSION_ID,
            new_message=user_query, #<= Pass the user query as new_message
        ):
        print("\nEvent Ttiggered: \n", event)

        if event.is_final_response():
          print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
          print("\nFinal Response....")
          if event.content and event.content.parts:
              print("\nAgent Response:\n", event.content.parts[0].text)
              print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
              # Define state changes
              # Response from the agent will be stored in the session state under the key 'response'
              state_changes = {'response': event.content.parts[0].text}

              # Create event with actions
              actions_with_update = EventActions(state_delta=state_changes)
              system_event = Event(
                invocation_id="invocation_id",
                author="system", # Or 'agent', 'tool' etc.
                actions=actions_with_update,
                timestamp=time.time()
              )

              # Append the event
              await session_service.append_event(session, system_event)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Check status of the session after the agent runs and the state is updated
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Await the get_session coroutine
    # Get information about the session after the agent runs
    existing_session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )

    print("\n\nSession State After the Agent Runs:\n", existing_session.state)

    print("\n\nSession Key-Value Pairs:")
    for key, value in existing_session.state.items():
        print(f"{key}: {value}")


    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Adding a new session with different context to the same InMemorySessionService

    NEW_SESSION_ID = str(uuid.uuid4())
    NEW_USER_ID = "soharabhossain"
    NEW_APP_NAME = "TalkerApp"

    new_state_context = {
        "user": "Soharab Hossain",
        "data": "Data is the new oil",
    }

    # Create a new session inside session_service which is of type InMemorySessionService
    # Await the coroutine to get the session object
    new_session = await session_service.create_session(
        app_name=NEW_APP_NAME,
        user_id=NEW_USER_ID,
        session_id=NEW_SESSION_ID,
        state=new_state_context, #<== Pass the state context to session object
    )

    print("New Session ID:", new_session.id) # Note this is `id` not `session_id`
    print("New Session App Name:", new_session.app_name)
    print("New Session User ID:", new_session.user_id)
    print("New Session State Before the Agent Runs:\n", new_session.state)

    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Check status of the session after the agent runs and the state is updated
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Await the get_session coroutine
    # Get information about the session after the agent runs
    new_existing_session = await session_service.get_session(
        app_name=NEW_APP_NAME,
        user_id=NEW_USER_ID,
        session_id=NEW_SESSION_ID,
    )

    print("\n\nNew Session State:\n", new_existing_session.state)

    print("\n\nNew Session Key-Value Pairs:")
    for key, value in new_existing_session.state.items():
        print(f"{key}: {value}")

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#--------------------------------------------
# Entry point for the script  
#--------------------------------------------
if __name__ == "__main__":
    asyncio.run(main())

