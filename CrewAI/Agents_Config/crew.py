
# MANUALLY create a folder structure 
 # > Create a root folder, e.g. `Agents_Config`
 # Create a subfolder `config` 
 # and create two files inside it `agents.yaml`` and `tasks.yaml`
 # create crew.py and main.py inside the folder `Agents_Config`
 # Run the project from `Agents_Config`foler using command `python main.py`


# WITHOUT using the standard CrewAI scaffolding with 
 #  `crewai create crew my_project` command and later
 # running it with `crewai run` command, etc.`)

# crew.py
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool
import yaml
import os

from dotenv import load_dotenv
load_dotenv()

#------------------------------------------------------------------------

# Create an LLM with a temperature of 0 to ensure deterministic outputs
# llm = LLM(model="gpt-4o-mini", temperature=0)
llm = LLM(model="groq/qwen/qwen3-32b", temperature=0.7)
# llm = LLM(model="groq/gemma2-9b-it", temperature=0.7)
#------------------------------------------------------------------------

#------------------------------------------------------------------------
class MyCrew():
    agents_config = yaml.safe_load(open(os.path.join("config", "agents.yaml"), "r"))
    tasks_config = yaml.safe_load(open(os.path.join("config", "tasks.yaml"), "r"))
    
    def researcher(self) -> Agent:
        return Agent(
            # config=self.agents_config["researcher"],
            **self.agents_config["researcher"],
             tools=[SerperDevTool()],
            llm=llm,
            allow_delegation=False,
            verbose=True
        )

    def writer(self) -> Agent:
        return Agent(
            config=self.agents_config["writer"],
            # **self.agents_config["writer"],
             llm=llm,
            allow_delegation=False,
            verbose=True
        )

    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_task"],
            agent=self.researcher(),
            verbose=True

        )

    def writing_task(self) -> Task:
        return Task(
            config=self.tasks_config["writing_task"],
            # **self.tasks_config["writing_task"],
            depends_on =[self.research_task()],
            agent=self.writer(),
            output_file="report.md",
            verbose=True
        )

    def crew(self) -> Crew:
        return Crew(
            agents=[self.researcher(), self.writer()],
            tasks=[self.research_task(), self.writing_task()],
            process=Process.sequential,
            verbose=True
        )
