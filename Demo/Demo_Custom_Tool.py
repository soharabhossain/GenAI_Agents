
import os
from crewai import Agent, Task, Crew, LLM

from dotenv import load_dotenv
load_dotenv()

#------------------------------------------------------------------------
# Create an LLM with a temperature of 0 to ensure deterministic outputs
# llm = LLM(model="gpt-4o-mini", temperature=0)
llm = LLM(model="groq/qwen/qwen3-32b", temperature=0.7)
# llm = LLM(model="groq/gemma2-9b-it", temperature=0.7)
#------------------------------------------------------------------------

from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
#-------------------------------------------------------------------
# Define a custom input data type for the tool
class MyToolInput(BaseModel):
    """Input schema for CustomTool."""
    tool_message: str = Field(..., description="This is a text message.")
    tool_number: int = Field(..., description="This is a number.")
#-------------------------------------------------------------------
# Define the tool
class CustomTool(BaseTool):
    name: str = "Custom Tool to echo message."
    description: str = "This tool echos message. It's vital for echoing messages."
    args_schema: Type[BaseModel] = MyToolInput

    def _run(self, tool_message: str, tool_number: int) -> str:
        # Your tool's logic here
        print("\n Runnnig custom tool......")
        return f"Echoing message: {tool_message}. Long live {tool_number} years + eternity!"
#-------------------------------------------------------------------
# Create agents with your tool
agent = Agent(
    role="Echo Agent",
    goal="Echo back input using custom tool",
    backstory="You are expert in echoing messages",
    tools=[CustomTool()],
    llm=llm,
    verbose=True
)

task = Task(
    description="Echo the provided message {message} {number}.",
    expected_output="You need to echo the message returned by the tool.",
    agent=agent,
    verbose=True
)

crew = Crew(agents=[agent], tasks=[task])
result = crew.kickoff(inputs={ "message": "Hello, India", "number": "1100"})
# result = crew.kickoff(inputs={ "number": "1100", "message": "Hello, India"})

print(result)


