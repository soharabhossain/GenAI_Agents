
#------------------
# DEMO: Using Tools
#------------------

from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool

from dotenv import load_dotenv
load_dotenv()

#------------------------------------------------------------------------

# Create an LLM with a temperature of 0 to ensure deterministic outputs
# llm = LLM(model="gpt-4o-mini", temperature=0)
llm = LLM(model="groq/qwen/qwen3-32b", temperature=0.7)
# llm = LLM(model="groq/gemma2-9b-it", temperature=0.7)

#------------------------------------------------------------------------
# Create tools
search_tool = SerperDevTool()

#------------------------------------------------------------------------

# Add tools to agent
researcher = Agent(
    role="Technology Researcher",
    goal="""Research the latest developments in {topic}""",
    backstory="""You are an experienced researcher known for thorough technical research and enlightning summary of the main technical points for a gven {topic}.""",
    llm=llm,
    tools=[search_tool],
    verbose=True
)

task = Task(
  description="""Find suitable information about {topic}""",
  expected_output="Good technical summary with insights as bullet points, followed by a summary.",
  agent = researcher
)

crew = Crew(
  agents=[researcher],
  tasks=[task],
  verbose=True
)

results = crew.kickoff(inputs={"topic": "Grok LLM from X.ai"})
print(results)

