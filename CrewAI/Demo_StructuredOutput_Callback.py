
#-----------------------------------
# DEMO: Structured Output + Callback
#-----------------------------------

from crewai import Agent, Crew, Task, Process, LLM, Process
from crewai_tools import SerperDevTool, DirectoryReadTool
from pydantic import BaseModel
from typing import List

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
# Create tools
search_tool = SerperDevTool()  # Search capability
docs_tool = DirectoryReadTool(directory='./blog-posts')  # Reads from local files

#------------------------------------------------------------------------
# Define the Output Class to ensure Structured output from the crew
# This will be used to validate the output of the tasks 

class ResearchFindings(BaseModel):
    main_points: List[str]
    key_technologies: List[str]
    societal_impact: str

class Report(BaseModel):
    title: str
    introduction: str
    body: str
    conclusion: str
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

writer = Agent(
    role='Content Writer',
    goal='Craft engaging report about the provided topic',
    backstory='A skilled writer with a passion for technology and its impact on humanity.',
    tools=[docs_tool],
    llm=llm,
    verbose=False
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
    expected_output=('A summary of recent developments including a unique perspective on their significance.'
        'Your output should contain the following:'
        'main_points: the main textual summary of the report'
        'key_technologies: key technologies enabling the change'
        'societal_impact: how it impacts the life of people and the society as a whole'),
    agent=researcher,
    callback=research_task_callback,  
    output_pydantic = ResearchFindings
)

writing_task = Task(
    description=("""Write an engaging report about a topic based on the research analyst's summary.
                    You will receive research output in JSON format from the researcher.
                    You need to extract the following piece of information from the object returned by the `research_task`
                    'main_points: the main textual summary of the report'
                    'key_technologies: key technologies enabling the change'
                    'societal_impact: how it impacts the life of people and the society as a whole'
                     'Use this information to write a comprehensive and engaging report.' 
                     """),
    expected_output=(
        "A structured report with title, introduction, body, and conclusion, "
        "written in a clear and engaging style."),    
    agent=writer,
    callback=writing_task_callback,  
    output_pydantic=Report,       # Structured output format
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

#-----------------------------------------------------------------------------
# Assemble a crew with planning enabled
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    verbose=False,
    process=Process.sequential,
    planning=True,  # Enable planning feature
    step_callback=crew_step_callback  # to be executed after every step of the Crew
)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#------------------------------------------------------------------------
# Run the Crew
results = crew.kickoff(
    inputs={"topic": "Social media and its impact on humans"}
    )

#------------------------------------------------------------------------
print("\n\n--- What's in Results ---\n")
obj_attr = dir(results)
for att in obj_attr:
    print(att)
print("\n--------------------------------------\n")

print("\n++++++++++++++++++++++++++++++++++++++++++++++++\n")
print("\n--- What's in Results Token Usage---")
print("\n Usage Tokens: ", results.token_usage)
print("\n--------------------------------------\n")

print("\n++++++++++++++++++++++++++++++++++++++++++++++++\n")
print("\n--- What's in Results output [1]/ Writing Task ---\n")
writing_task_output = results.tasks_output[1]  # Task executed second i.e., writing_task
print("Task Description:", writing_task_output.description)
print("\n--------------------------------------------------------")
# report = writing_task_output.pydantic # OR the next statement means the same
report = results.pydantic # Results/Output of the Last Task executed by the Crew, i.e., writing_task
                          # `results` hold the information about the LAST EXECUTED task which is writing task 
print("\n--- What's in Results Tasks Output[1] / Pydantic---")
print(f"\n Report Title: {report.title}")
print(f"\n Report Introduction: {report.introduction}")
print(f"\n Report Body: {report.body}")
print(f"\n Report Conclusion: {report.conclusion}")

print("\n++++++++++++++++++++++++++++++++++++++++++++++++\n")

print("\n--- What's in Results Task output [0]/ Research Task ---\n")
research_task_output = results.tasks_output[0]  # Task executed first i.e., research_task
# print(dir(research_task_output))
print("Task Description:", research_task_output.description)
print("\n--------------------------------------------------------")
research = research_task_output.pydantic
# print(type(research))
print(f"\n Main Points: {research.main_points}")
print(f"\n Key Technologies: {research.key_technologies}")
print(f"\n Societal Impact: {research.societal_impact}")

print("\n++++++++++++++++++++++++++++++++++++++++++++++++\n")
"""
#------------------------------------------------------------
# Verify successful context passing between the agents
#------------------------------------------------------------

# Extract the outputs of individual tasks
research_output = results.tasks_output[0].pydantic
writing_output = results.tasks_output[1].pydantic

# --- Verification Logic ---
# Check if the research output is a valid Pydantic model
if not isinstance(research_output, ResearchFindings):
    print("❌ Research task did not produce a valid ResearchFindings object.")
else:
    print("✅ Research task produced a valid ResearchFindings object.")

    # Get a specific piece of information from the research findings
    # For example, the first main point or a key technology
    key_research_point = research_output.main_points[0] if research_output.main_points else ""
    key_technology = research_output.key_technologies[0] if research_output.key_technologies else ""
    
    print(f"\nKey research point to check: '{key_research_point}'")
    print(f"\nKey technology to check: '{key_technology}'")

    # Check if the writing output is a valid Pydantic model
    if not isinstance(writing_output, Report):
        print("❌ Writing task did not produce a valid Report object.")
    else:
        print("✅ Writing task produced a valid Report object.")
        
        # Now, verify if the writer's report contains the information from the researcher
        # This is the core of the verification
        if key_research_point in writing_output.body or key_research_point in writing_output.introduction:
            print("🎉 SUCCESS: The writer's report successfully incorporated the research context!")
        else:
            print("⚠️ The writer's report seems to be missing the key research context.\n\n")
    
"""    
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
