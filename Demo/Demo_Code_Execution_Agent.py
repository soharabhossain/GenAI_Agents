
from crewai import Agent, Task, Crew, LLM

from dotenv import load_dotenv
load_dotenv()

#------------------------------------------------------------------------
# Option-1 - The EASY way
#------------------------------------------------------------------------
#------------------------------------------------------------------------
# Create an LLM with a temperature of 0 to ensure deterministic outputs
# llm = LLM(model="gpt-4o-mini", temperature=0)
llm = LLM(model="groq/qwen/qwen3-32b", temperature=0.7)
# llm = LLM(model="groq/gemma2-9b-it", temperature=0.7)
#------------------------------------------------------------------------
# Define the agent with code execution mode enabled
python_agent = Agent(
    role="Python Executor",
    goal="Execute any Python code provided in the task",
    backstory="You are a skilled Python interpreter capable of running code directly.",
    code_execution_mode="safe",  # Enables direct Python code execution
    llm=llm
)
#---------------------------------------------------------------
# Define a Python code block as the task
python_code = """
# Calculate the sum of first 10 numbers
total = sum(range(1, 11))
print("Sum of 1 to 10:", total)
"""
#---------------------------------------------------------------
# Create the task for the agent
task = Task(
    description=f"Run this Python code and return the output:\n```python\n{python_code}\n```",
    expected_output="Result of code execution",
    agent=python_agent
)
#---------------------------------------------------------------
# Create the crew with the single agent
crew = Crew(
    agents=[python_agent],
    tasks=[task]
)

# Run the crew
result = crew.kickoff()
print("Execution Result:", result)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

"""
from crewai import Agent, Task, Crew, LLM
from crewai.tools import BaseTool
import io
import contextlib

#------------------------------------------------------------------------
# Option-2
#------------------------------------------------------------------------
# Create a simple Python code execution tool
class PythonExecutorTool(BaseTool):
    name: str = "Python Executor"
    description: str = "Executes Python code and returns the output."

    def _run(self, code: str) -> str:
        try:
            # Capture stdout
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                exec(code, {})
            return buffer.getvalue().strip() or "Code executed successfully (no output)."
        except Exception as e:
            return f"Error during execution: {str(e)}"
#------------------------------------------------------------------------
# Define the code execution agent
executor_agent = Agent(
    role="Code Executor",
    goal="Execute Python code provided in the task and return the result.",
    backstory="An expert Python programmer capable of running and testing code snippets.",
    tools=[PythonExecutorTool()],
    llm=llm,
    verbose=True
)
#-------------------------------------
# 3. Define a task for the agent

task = Task(
    # description="Execute the following Python code:\nprint(sum([1, 2, 3, 4])*10)",

    description="Execute the following Python code: {code})",
    expected_output="Computed result",
    agent=executor_agent,

)

#------------------------------------------------------------------------
# code_block = """
# ```python
# # This is a simple Python code block
# name = "World"
# print(f"Hello, {name}!") 
# ```
# """

"""
# 4. Create and run the crew
crew = Crew(
    agents=[executor_agent],
    tasks=[task],
    verbose=True
)

# result = crew.kickoff()
result = crew.kickoff(inputs={"code": code_block})
print("\nFinal Result:", result)


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
"""

