import os

from dotenv import load_dotenv
load_dotenv()

from google.adk.agents import Agent

root_agent = Agent(
    name="AI_Post_Agent",
    description="An agent that knows some things about the user and their posts preferences",
    model=os.environ.get("GEMINI_MODEL"),
    instruction="""
    You are a helpful assistant that can respond about the user and their preferences.
    The information about the user and their preferences is given in the state context.
    Name: {user}
    Preference: {preference} in the style of {style}
    """,
)