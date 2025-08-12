
#---------------------------------------------
# DEMO: Hierarchical process (with Tools call)
#---------------------------------------------

import os
from crewai import Agent, Task, Crew, LLM, Process
from crewai_tools import SerperDevTool, DirectoryReadTool

from dotenv import load_dotenv
load_dotenv()


# -----------
# Create LLM
# -----------
manager_llm = LLM(model="openai/gpt-4o", temperature=0.3) # Make sure to use a more capable LLM here
llm = LLM(model="groq/qwen/qwen3-32b", temperature=0.3)

#------------------------------------------------------------------------
# Instantiate the Tools
search_tool = SerperDevTool()
docs_tool = DirectoryReadTool(directory='./blog-posts')
# ---------------------------------------------------

# --------------
# Define Agents
# --------------
manager_agent = Agent(
    role="Content Manager",
    goal="Coordinate the blog creation process by assigning subtasks to the research specialist and content writer agents.",
    backstory=(
        "You are an experienced content manager. "
        "You decide the order of work, delegate to other coworker agents, and ensure the final task completion."
        "You do NOT solve the problem on your own. You need to coordinate amongst the coworker agents to get the task completed."
        "Ideally you should kick off the researcher first to collect information and then pass the research findings to the content writer agent."
        "Coworker agents may have access to specific tools that they should use to complete their tasks."
    ),
    llm=manager_llm, # Make sure to use a more capable LLM here
    max_iter=3,
    allow_delegation=True,
    verbose=True
)

research_agent = Agent(
    role="Research Specialist",
    goal="Gather accurate and relevant information in real-time for a given topic.",
    backstory="You are an expert in web research, skilled at finding key facts, statistics, and trends.",
    llm=llm,
    max_iter=3,
    tools=[search_tool],
    allow_delegation=False,
    verbose=True
)

writer_agent = Agent(
    role="Content Writer",
    goal="Produce high-quality blog articles from the provided research material.",
    backstory="You write clear, engaging, and well-structured content.",
    llm=llm,
    tools=[docs_tool],
    max_iter=3,
    max_rpm=15,
    allow_delegation=False,
    verbose=True
)

# --------------------
# Define Tasks
# --------------------
research_task = Task(
    description=(
        "Research the topic '{topic}'. Provide 5-7 bullet points "
        "with key facts, statistics, and relevant examples."
        "Use the provided tool to search for the latest information about the topic. "
        "Do NOT rely on memory — you must call the search tool at least once."
    ),
    expected_output="A bullet-point list of factual research notes.",
    agent=research_agent,
    verbose=True

)

writing_task = Task(
    description=(
        "Write a 500-word blog post on '{topic}' using this research done by the researcher."
    ),
    expected_output="A fully written blog post.",
    agent=writer_agent,

    # Let the manager pass the context as required. 
    # You do not need to set any order of execution of the agents/tasks or pass the context
    # DO NOT SET THE FOLLOWING ATTRIBUTES
    # depends_on=[research_task],
    # context = [research_task], # This passes the context of the research task as a Task object not as strings as expected by the writin agent
                                 # Comment this line and just use depends_on to pass the context as a string 

    output_file="blog-posts/new_tech_post_{topic}.md",  # The final blog post will be saved here
    verbose=True
)

# -------------------------------------
# Define Crew with Hierarchical Process
# -------------------------------------
crew = Crew(
    agents=[research_agent, writer_agent], # We do NOT specify the manager agent in this list
    tasks=[research_task, writing_task],
    process=Process.hierarchical,    # <--- THIS sets the hierarchical workflow
    manager_agent=manager_agent,     # <--- EITHER Explicitly set the manager agent
    # manager_llm="openai/gpt-4o", # <--- OR Explicitly set the manager LLM, make sure to use a more capable LLM here
    planning=True,
    verbose=True
)

# -------------
# Run the Crew
# -------------
result = crew.kickoff(inputs={"topic": "The future of job market for CS undergrad in the era of Gen AI"})
# result = crew.kickoff(inputs={"topic": "The future of Humanity as we tend to achieve AGI"})
# result = crew.kickoff(inputs={"topic": "About OpenAI's latest GPT-5 model. Major technical heighlights as 5 bullet points. Additional 3 bullet points highlighting how it is better than GPT-4"})

print("\n=== FINAL OUTPUT ===")
print(result)

