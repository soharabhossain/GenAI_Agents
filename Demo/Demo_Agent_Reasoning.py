
from crewai import Agent, Task, Crew, LLM

from dotenv import load_dotenv
load_dotenv()

#------------------------------------------------------------------------
import warnings
warnings.filterwarnings("ignore")
#------------------------------------------------------------------------

import logging
# Set up logging to capture any reasoning errors
logging.basicConfig(level=logging.INFO)

#------------------------------------------------------------------------

# Create an LLM with a temperature of 0 to ensure deterministic outputs
# llm = LLM(model="gpt-4o-mini", temperature=0)
llm = LLM(model="groq/qwen/qwen3-32b", temperature=0.7)
# llm = LLM(model="groq/gemma2-9b-it", temperature=0.7)

#------------------------------------------------------------------------

# Create an agent with reasoning enabled
analyst = Agent(
    role="Data Analyst",
    goal="Analyze data and provide insights",
    backstory="You are an expert data analyst.",
    reasoning=True,
    max_reasoning_attempts=3,  # Optional: Set a limit on reasoning attempts
    llm=llm
)

# Create a task
analysis_task = Task(
    description="Analyze the provided sales data and identify key trends.",
    expected_output="A report highlighting the top 3 sales trends.",
    agent=analyst
)

# ---------------------------------------------------------------------------
# Execute the task by the agent
# If an error occurs during reasoning, it will be logged and execution will continue
result = analyst.execute_task(analysis_task)

# ---------------------------------------------------------------------------
# Create a crew and run the task
crew = Crew(agents=[analyst], tasks=[analysis_task])
result = crew.kickoff()

print(result)
# -----------------------------------------------------------------------------------