"""
Knowledge in CrewAI is a powerful system that allows AI agents to access and utilize external information sources 
during their tasks. Think of it as giving your agents a reference library they can consult while working.
"""
# All the source files reside inside a `knowledge` folder in the current directory.

from dotenv import load_dotenv
load_dotenv()


from crewai import Agent, Task, Crew, Process, LLM
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource 

#pip install docling
from crewai.knowledge.source.crew_docling_source import CrewDoclingSource

#------------------------------------------------------------------------------------
# Create a knowledge source
content = "Users name is John. He is 30 years old and lives in San Francisco."
string_source = StringKnowledgeSource(content=content)

# Create a knowledge source from web content
content_source = CrewDoclingSource(
    file_paths=[
        "https://lilianweng.github.io/posts/2024-11-28-reward-hacking",
        "https://lilianweng.github.io/posts/2024-07-07-hallucination",
    ],
)
#------------------------------------------------------------------------------------
# Similarly use othe sources of knowledge
#------------------------------------------------------------------------------------
# Text File Knowledge Source
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource
text_source = TextFileKnowledgeSource(
    file_paths=["Document.txt", "Another.txt"]
)
#------------------------------------------------------------------------------------
# PDF Knowledge Source
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
pdf_source = PDFKnowledgeSource(
    file_paths=["YoloXNet.pdf", "YoloXNet_n_Others.pdf"]
)
#------------------------------------------------------------------------------------
# CSV File Knowledge Source
from crewai.knowledge.source.csv_knowledge_source import CSVKnowledgeSource
csv_source = CSVKnowledgeSource(
    file_paths=["CSV_Data.csv"] # IRIS flower dataset
)
#------------------------------------------------------------------------------------
# Excel File Knowledge Source
from crewai.knowledge.source.excel_knowledge_source import ExcelKnowledgeSource
excel_source = ExcelKnowledgeSource(
    file_paths=["Excel_Data.xlsx"] # IRIS flower dataset
)
#------------------------------------------------------------------------------------
# JSON File Knowledge Source
from crewai.knowledge.source.json_knowledge_source import JSONKnowledgeSource
json_source = JSONKnowledgeSource(
    file_paths=["JSON_Data.json"]
)
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
# Create an LLM with a temperature of 0 to ensure deterministic outputs
# llm = LLM(model="gpt-4o-mini", temperature=0)
llm = LLM(model="groq/qwen/qwen3-32b", temperature=0.7)
# llm = LLM(model="groq/gemma2-9b-it", temperature=0.7)

# Create an agent with the knowledge store
agent = Agent(
    role="AI Agent",
    goal="You answer user queries.",
    backstory="You are an expert chatbot. You look for available knowledge to answer user queries.",
    verbose=False,
    allow_delegation=False,
    llm=llm,
    # knowledge_sources=[string_source, text_source, pdf_source, csv_source, excel_source, json_source], # Enable knowledge by adding the sources here
    knowledge_sources=[text_source, json_source], # Enable knowledge by adding the sources here
)

task = Task(
    description="Answer the following question: {question}",
    expected_output="A contextual answer to the question. Look for available knowledge to answer the question.",
    agent=agent,
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=False,
    process=Process.sequential,
    # knowledge_sources=[string_source], # Enable knowledge by adding the sources here
)

# result = crew.kickoff(inputs={"question": "What city does John live in and how old is he?"})
# result = crew.kickoff(
#     inputs={"question": "What is the reward hacking paper about? Be sure to provide sources."}
# )

    # "What's the third data point mentioned in the `CSV_Data.csv`` file?",
    # "What's the data sample with longest petal length?",
    # "What's the value for sepal length for the last data point in the `CSV_Data.csv` file?",
    # "What is the reward hacking paper about? Be sure to provide sources.",
    # "Summarize the content of `Another.txt``.",
    # "Check the attached pdf YoloXNet_n_Others.pdf and tell me how does YoloXNet compare with other models?",

questions = [
    "What is the main topic discussed in the file `Document.txt`?", 
    "what's the age of John Doe?",
]

for question in questions:
    result = crew.kickoff(inputs={"question": question})
    print(f"Q: {question}\nA: {result}\n")
