#----------------------------------------------------------
# DEMO: Agent execution wthout defining explicit Task object
#----------------------------------------------------------

from crewai import Agent, LLM
from crewai.tools import tool 
from pydantic import BaseModel, Field

from dotenv import load_dotenv
load_dotenv()

# --------------------------------------------------
# 1. Define LLM clients
# --------------------------------------------------
# research_llm = LLM(model="openai/gpt-4o-mini", temperature=0.3)
llm = LLM(model="groq/qwen/qwen3-32b", temperature=0.3)

# --------------------------------------------------
# 2. Define a tool
# --------------------------------------------------
@tool
def multiply_numbers(a: int, b: int) -> int:
    """Multiplies two integers."""
    return a * b

# --------------------------------------------------
# 3. Define structured output schema
# --------------------------------------------------
class MathResult(BaseModel):
    a: int = Field(..., description="The first number")
    b: int = Field(..., description="The second number")
    product: int = Field(..., description="The result of multiplying a and b")
# --------------------------------------------------

# 4. Create the agent with tool + structured output
agent = Agent(
    role="Math Assistant",
    goal="Given two integers, return them and their product as structured output",
    backstory="You are great at math and always use the multiplication tool.",
    verbose=True,
    allow_delegation=False,
    llm=llm,
    tools=[multiply_numbers],
    output_json= MathResult  # Structured output!
)

# --------------------------------------------------

# 5. Kickoff agent directly (no Task object)
# 5. Kickoff agent directly (prompt only, no Task)
result = agent.kickoff(
    "Multiply 7 and 6 and return the numbers and product in structured form.",
    # response_format=MathResult # This is redundant since we already defined output_json in the Agent
)

print(result)
