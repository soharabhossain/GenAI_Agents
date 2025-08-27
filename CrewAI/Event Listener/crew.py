# Import your custom event listener
from MyEventListener import MyCustomListener

# Create an instance of your listener
my_listener = MyCustomListener()

#---------------------------------------
# Define the Crew
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

#---------------------------------------
from dotenv import load_dotenv
load_dotenv()
from crewai_tools import SerperDevTool
search_tool = SerperDevTool()
#---------------------------------------

@CrewBase
class LatestAIDevelopmentCrew():
  """LatestAIDevelopment crew"""

  @agent
  def researcher(self) -> Agent:
    return Agent(
      config=self.agents_config['researcher'], # type: ignore[index]
      verbose=True,
      tools=[search_tool]
    )

  @agent
  def reporting_analyst(self) -> Agent:
    return Agent(
      config=self.agents_config['reporting_analyst'], # type: ignore[index]
      verbose=True
    )

  @task
  def research_task(self) -> Task:
    return Task(
      config=self.tasks_config['research_task'] # type: ignore[index]
    )

  @task
  def reporting_task(self) -> Task:
    return Task(
      config=self.tasks_config['reporting_task'] # type: ignore[index]
    )

  @crew
  def crew(self) -> Crew:
    return Crew(
      agents=[
        self.researcher(),
        self.reporting_analyst()
      ],
      tasks=[
        self.research_task(),
        self.reporting_task()
      ],
      process=Process.sequential
    )