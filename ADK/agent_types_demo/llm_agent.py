# DEMO: LLM AGENT

#---------------------------------------------------------------------
# LlmAgent - A simple agent that uses a tool to answer questions.
# Run this demo with: `adk web`
#---------------------------------------------------------------------
from google.adk.agents import LlmAgent
from google.adk.tools import google_search

root_agent = LlmAgent(
    model="gemini-2.0-flash-exp", # Required: Specify the LLM
    name="question_answer_agent", # Required: Unique agent name
    description="A helpful assistant agent that can answer questions.",
    instruction="Respond to the query using google search",
    tools=[google_search], # Provide an instance of the tool
)


