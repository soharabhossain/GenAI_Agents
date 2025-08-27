

#------------------------------------------------------------
# DEMO: Context Passing - Custom Logging Agent, Step Callback
#------------------------------------------------------------

from crewai import Agent, Crew, Task, Process, LLM
from crewai_tools import SerperDevTool, DirectoryReadTool

from dotenv import load_dotenv
load_dotenv()

#------------------------------------------------------------------------
import warnings
warnings.filterwarnings("ignore")
#------------------------------------------------------------------------
# Create an LLM with a temperature of 0 to ensure deterministic outputs
# llm = LLM(model="gpt-4o-mini", temperature=0)
llm = LLM(model="groq/qwen/qwen3-32b", temperature=0.7)
# llm = LLM(model="groq/gemma2-9b-it", temperature=0.7)

#------------------------------------------------------------------------
# Create Tools
search_tool = SerperDevTool()  # Search capability
docs_tool = DirectoryReadTool(directory='./blog-posts')  # Reads from local files

# ----------------------------------------------------------------------------------------------
# Define Custom Logging Agent
# To use this agent, make sure to import datetime

from crewai import Agent
from datetime import datetime
import json
# ----------------------------------------------------------------------------------------------

class LoggingAgent(Agent):
    log_file: str = Field(default="agent_logs.log", description="Path to the agent's log file")

    def execute_task(self, task, context=None, **kwargs):
        try:
            if hasattr(context, "model_dump_json"):
                context_str = context.model_dump_json(indent=2)
            elif isinstance(context, list):
                context_str = json.dumps(
                    [c.model_dump() if hasattr(c, "model_dump") else str(c) for c in context],
                    indent=2
                )
            else:
                context_str = str(context)
        except Exception as e:
            context_str = f"<Could not serialize context: {e}>"

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent_role": self.role,
            "task_description": task.description,
            "context_received": context_str
        }

        print("\n--- LOGGING AGENT: CONTEXT RECEIVED ---")
        print(context_str)
        print("---------------------------------------\n")

        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False, indent=2))
            f.write("\n")

        # Pass through all args/kwargs to the base class
        return super().execute_task(task, context=context, **kwargs)

#------------------------------------------------------------------------
# Create Agents
researcher = Agent(
    role='Research Analyst',
    goal='Use available tool to collect information and provide up-to-date technical and social analysis on a given topic',
    backstory='An expert analyst with a keen eye for technical nitty-gritty with a perspective on human vakues.',
    tools=[search_tool],
    llm=llm,
    verbose=False
)

#------------------------------------------------------------------------------------------
# writer = Agent(
#     role='Content Writer',
#     goal='Craft engaging report about the provided topic',
#     backstory='A skilled writer with a passion for technology and its impact on humanity.',
#     tools=[docs_tool],
#     llm=llm,
#     verbose=False
# )

writer = LoggingAgent(
    log_file='writer_context.json',
    role='Content Writer',
    goal='Craft engaging report about the provided topic',
    backstory='A skilled writer with a passion for technology and its impact on humanity.',
    tools=[docs_tool],
    llm=llm,
    verbose=False,
)


#----------------------------------------------------------------------------------
#------------------------------------------------------------------------
# Define callbacks for tasks
def research_task_callback(output):
    print("\n--- Research Task Completed ---")
    print("Research Output Type:", type(output))
    print("Research Output:")
    print(output.model_dump_json(indent=2))

def writing_task_callback(output):
    print("\n--- Writing Task Completed ---")
    print("Writing Output Type:", type(output))
    print("Writing Output:")
    print(output.model_dump_json(indent=2))

#------------------------------------------------------------------------
# Define tasks
research_task = Task(
    description='Research the latest trends in the topic {topic}',
    expected_output=("""A summary of recent developments formatted strictly as a single Markdown-formatted text block with the following sections and content:

    # Main Points
    - [main point 1]
    - [main point 2]
    - [main point 3]

    # Key Technologies
    - [technology 1]
    - [technology 2]
    - [technology 3]

    # Societal Impact
    [a comprehensive paragraph detailing the societal impact]
    """),
    agent=researcher,
    # callback=research_task_callback,
    verbose=True
)

writing_task = Task(
    description=("""You will receive a research summary from the Research Analyst. The summary is strictly formatted with Markdown headings for 'Main Points', 'Key Technologies', and 'Societal Impact'.
    Your task is to:
    1.  Read the entire research summary provided by the Research Analyst.
    2.  Extract the content under each of the Markdown headings.
    3.  Use the extracted 'Main Points', 'Key Technologies', and 'Societal Impact' to write a comprehensive and engaging report.
    """),
    expected_output=(
        "A report with title, introduction, body, and conclusion, written in a clear and engaging style."),    
    agent=writer,
    # callback=writing_task_callback,  
    output_file='blog-posts/report.md',  # The final blog post will be saved here 
    # depends_on=[research_task],  
    context = [research_task], # Pass research context to writer
    verbose=True
)
#------------------------------------------------------------------------
# Step Callback for the Crew
def crew_step_callback(output):
    """A sample step callback function."""
    print("--- CREW CALLBACK: STEP COMPLETED ---")
    print(output)
    print("----------------------")
#---------------------------------------------------
def crew_step_callback_serialize(output):
    """
    A step callback that serializes the output to a JSON file.
    """
    # The file name can be dynamic or static.
    # For simplicity, we'll use a static file name.
    output_file = "crew_steps.log"

    # The output from the callback can be a Pydantic model, a string, or other types.
    # We'll handle a few common cases.
    if hasattr(output, 'model_dump'):
        # If it's a Pydantic model, convert it to a dictionary.
        output_data = output.model_dump()
    elif isinstance(output, str):
        # If it's a string, we can just log it directly.
        output_data = {"raw_output": output}
    else:
        # Fallback for other types.
        output_data = {"unserializable_output": str(output)}

    # Open the file in append mode ('a') to add to it each time.
    with open(output_file, 'a') as f:
        # Write a separator and the JSON data.
        f.write("--- STEP COMPLETED ---\n")
        json.dump(output_data, f, indent=2)
        f.write("\n\n")

#-----------------------------------------------------------------------------
# Assemble a crew with planning enabled
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    verbose=True,
    process=Process.sequential,
    planning=True,  # Enable planning feature
    # step_callback=crew_step_callback,  
    step_callback=crew_step_callback_serialize
)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#------------------------------------------------------------------------
# Run the Crew
results = crew.kickoff(
    inputs={"topic": "Social media and its impact on humans"}
    )

#------------------------------------------------------------------------
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Get the outputs of the research and writing tasks
research_output = results.tasks_output[0].raw
writing_output = results.tasks_output[1].raw

# Perform a simple check
# Check if a key phrase from the research output is present in the writer's output
if "societal impact" in research_output and "societal impact" in writing_output:
    print("✅ Context seems to have been passed and used by the writer.")
else:
    print("❌ Context may not have been passed or used correctly.")