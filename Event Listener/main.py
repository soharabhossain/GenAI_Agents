
import sys
from datetime import datetime

from crew import LatestAIDevelopmentCrew

from dotenv import load_dotenv
load_dotenv()

import warnings
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        # 'topic': 'Ambient Agents in LangChain',
        'topic': 'GPT-5 by OpenAI',
        'current_year': str(datetime.now().year)
    }
    
    try:
        LatestAIDevelopmentCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


if __name__== "__main__":
    run()
