
# ---------------------------------------------------
# DEMO: Logging Tool Calling with Runtime Safeguard
# ---------------------------------------------------

import datetime
from typing import Optional
from pydantic import Field
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool, DirectoryReadTool

from dotenv import load_dotenv
load_dotenv()

# ------------------------------------------------
# 1. Define a logging wrapper with file saving
# ------------------------------------------------

class LoggingSerperTool(SerperDevTool):
    was_used: bool = Field(default=False, description="Flag to check if the tool was used")
    log_file: Optional[str] = Field(default="tool_invocations.log", description="Path to local log file")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Clear log at start
        with open(self.log_file, "w", encoding="utf-8") as f:
            f.write(f"=== Tool Invocation Log ({datetime.datetime.now()}) ===\n")

    def log_to_file(self, message):
        """Append a log entry to the local log file."""
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(message + "\n")

    def _run(self, *args, **kwargs):
        """Intercept tool execution to set flag and log usage."""
        object.__setattr__(self, "was_used", True)  # bypass Pydantic restrictions

        # Log the invocation
        log_entry = f"[{datetime.datetime.now()}] Tool invoked with args: {args}, kwargs: {kwargs}"
        print(log_entry)
        self.log_to_file(log_entry)

        # Call the original SerperDevTool functionality
        result = super()._run(*args, **kwargs)

        # Log the result
        result_log = f"[{datetime.datetime.now()}] Tool returned results: {result}"
        print(result_log)
        self.log_to_file(result_log)

        return result

#-----------------------------------------------------------------------

# Create instance of logging tool
search_tool = LoggingSerperTool(log_file="search_tool_usage_log.txt")
docs_tool = DirectoryReadTool(directory="./blog-posts")

# --------------------------------------------------
# 2. Define LLM clients
# --------------------------------------------------
research_llm = LLM(model="openai/gpt-4o-mini", temperature=0.3)
llm = LLM(model="groq/qwen/qwen3-32b", temperature=0.3)


# ------------------------------------------------
# 3. Create agents
# ------------------------------------------------
researcher = Agent(
    role="Researcher",
    goal="You utilize the available tool to collect the most latest information about the given topic.",
    backstory="An expert in searching the web for the latest news about the given topic.",
    tools=[search_tool],  # Attach logging tool
    llm=research_llm,
    allow_delegation=False,
    verbose=True
)

writer = Agent(
    role="Writer",
    goal="Create a short article from research notes.",
    backstory="Specializes in summarizing research findings into blog posts.",
    llm=llm,
    tools=[docs_tool],
    allow_delegation=False,
    verbose=True
)


# ------------------------------------------------
# 4. Create tasks
# ------------------------------------------------
research_task = Task(
    description="Use the search tool to find the most recent news about {topic}. Include URLs and dates.",
    expected_output="A bullet-point list about {topic} with sources and timestamps.",
    agent=researcher,
    verbose=True
)

writing_task = Task(
    description="Write a 200-word news summary article based on the researcher's findings.",
    expected_output="A concise article summarizing the research notes.",
    agent=writer,
    output_file="blog-posts/new_tech_post_{topic}.md",
    depends_on=[research_task],
    verbose=True
)


# ------------------------------------------------
# 5. Orchestrate the crew
# ------------------------------------------------
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process=Process.sequential,
    verbose=True
)


# ------------------------------------------------
# 6. Run with safeguard
# ------------------------------------------------
if __name__ == "__main__":
    result = crew.kickoff(
        inputs={"topic": "Application of Generative AI in Cyber Security Research"}
    )

    # Runtime safeguard
    if not search_tool.was_used:
        raise RuntimeError(
            "🚨 Search tool was NEVER invoked! The Researcher may have hallucinated the data."
        )

    print("\n=== FINAL OUTPUT ===")
    print(result)

    print(f"\n📂 Log saved to: {search_tool.log_file}")




