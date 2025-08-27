# ----------------------------
# DEMO: Agents with Memory
# ----------------------------

from crewai import Agent, Task, Crew, LLM
from pydantic import BaseModel, Field
import os

from dotenv import load_dotenv
load_dotenv()

#-------------------------------------------------------------------------
# ----- Define Pydantic Output Models -----
class StartupIdea(BaseModel):
    idea: str = Field(..., description="One creative startup idea")
    category: str = Field(..., description="Business category")

class MarketReport(BaseModel):
    market_size: str = Field(..., description="Information about the market size for the startup idea")
    competition: str = Field(..., description="Information about the market competitors")
    risks: str = Field(..., description="Information about the associated risks in the business")

class BusinessPlan(BaseModel):
    summary: str = Field(..., description="Summary of the business plan")
    target_audience: str = Field(..., description="Research about the target audience")
    monetization_strategy: str = Field(..., description="Monetization strategy for the start up")
#-------------------------------------------------------------------------
# ----- LLM -----
# Create an LLM with a temperature of 0 to ensure deterministic outputs
llm = LLM(model="gpt-4o-mini", temperature=0)
# llm = LLM(model="groq/qwen/qwen3-32b", temperature=0.7)
# llm = LLM(model="groq/gemma2-9b-it", temperature=0.7)

#-------------------------------------------------------------------------
from crewai.memory import LongTermMemory
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage

# Configure custom storage location
custom_storage_path = "./storage"
os.makedirs(custom_storage_path, exist_ok=True)

#-------------------------------------------------------------------------
# ----- Agents -----
idea_generator = Agent(
    role="Startup Idea Generator",
    goal="Generate an original startup idea",
    backstory="You are a creative entrepreneur with a knack for new ideas.",
    llm=llm
)

market_analyst = Agent(
    role="Market Analyst",
    goal="Analyze market potential of a startup idea",
    backstory="You specialize in understanding markets and business landscapes.",
    llm=llm
)

business_plan_writer = Agent(
    role="Business Plan Writer",
    goal="Write a concise business plan using the startup idea and market analysis",
    backstory="You are a professional business plan consultant.",
    llm=llm
)

#-------------------------------------------------------------------------
# ----- Tasks -----
task1 = Task(
    description="Generate one innovative startup idea with its business category.",
    expected_output="""An innovative startup idea in the required structured format.""",
    agent=idea_generator,
    output_pydantic=StartupIdea,
)

task2 = Task(
    description="Analyze the market potential for the startup idea stored in memory.",
    expected_output="""A market analysis report in the required structured format.""",
    agent=market_analyst,
    output_pydantic=MarketReport,
    # context =[task1]
)

task3 = Task(
    description=(
        "Using the startup idea and market analysis stored in memory, "
        "write a concise business plan."
    ),
    expected_output="""A concise business plan in the required structured format.""",
    agent=business_plan_writer,
    output_pydantic=BusinessPlan,
    # context = [task1, task2]
)

#-------------------------------------------------------------------------
# ----- Crew -----
crew = Crew(
    agents=[idea_generator, market_analyst, business_plan_writer],
    tasks=[task1, task2, task3],
    memory=True, # < -- set memory to True
    long_term_memory=LongTermMemory(
                                    storage=LTMSQLiteStorage( db_path=f"{custom_storage_path}/memory.db")
                              ),
    cache=True, # <-- caching enabled
    verbose=True
)

result = crew.kickoff()
print("\n--- Final Output ---")
print(result)
print("\n\n")
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------

# for agent in crew.agents:
#     if hasattr(agent, "memory") and agent.memory:
#         print(f"\n--- Memory for Agent: {agent.role} ---")
#         for m in agent.memory.dump():
#             print(m)

#-------------------------------------------------------------------------
#-------------------------------------------------------------------------



