
# DEMO:
# Define an agent that will be remotely accessible via A2A 
# We will spin a ADK API server to host this agent.
# To run the server, use the command: 
# adk api_server --a2a --port 8001 ./a2a_basic/remote_a2a
#----------------------------------------------------------------------------

import random

from google.adk import Agent
from google.adk.tools.tool_context import ToolContext
from google.genai import types


#----------------------------------------------------------------------------
# Define a tool to check if numbers are prime.
async def check_prime(nums: list[int]) -> str:
  """Check if a given list of numbers are prime.

  Args:
    nums: The list of numbers to check.

  Returns:
    A str indicating which number is prime.
  """
  primes = set()
  for number in nums:
    number = int(number)
    if number <= 1:
      continue
    is_prime = True
    for i in range(2, int(number**0.5) + 1):
      if number % i == 0:
        is_prime = False
        break
    if is_prime:
      primes.add(number)
  return (
      'No prime numbers found.'
      if not primes
      else f"{', '.join(str(num) for num in primes)} are prime numbers."
  )

#----------------------------------------------------------------------------
# Define the agent that uses the check_prime tool.
root_agent = Agent(
    model='gemini-2.0-flash',
    name='check_prime_agent', #<-- this is the name used to call the agent via A2A, mentioned in the agent card
    description='check prime agent that can check whether numbers are prime.',
    instruction="""
      You check whether numbers are prime.
      When checking prime numbers, call the check_prime tool with a list of integers. Be sure to pass in a list of integers. You should never pass in a string.
      You should not rely on the previous history on prime results.
    """,
    tools=[
        check_prime,
    ],
    # planner=BuiltInPlanner(
    #     thinking_config=types.ThinkingConfig(
    #         include_thoughts=True,
    #     ),
    # ),
    generate_content_config=types.GenerateContentConfig(
        safety_settings=[
            types.SafetySetting(  # avoid false alarm about rolling dice.
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=types.HarmBlockThreshold.OFF,
            ),
        ]
    ),
)
