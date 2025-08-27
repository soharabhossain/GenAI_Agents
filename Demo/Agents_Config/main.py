# main.py
from crew import MyCrew

def run():
    inputs = {"topic": "Generative AI Applications"}

    # Directly kickoff the crew as follows
    # MyCrew().crew().kickoff(inputs=inputs)

    # Alternatively
    crew_instance = MyCrew()
    my_crew = crew_instance.crew()
    results = my_crew.kickoff(inputs=inputs)

if __name__ == "__main__":
    run()
