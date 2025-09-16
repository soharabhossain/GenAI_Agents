from google.adk.agents import Agent
from google.adk.tools import google_search

# Define tool functions
# Fetch current date and time
def get_current_date_and_time() -> dict:
    """
    Returns the current date and time in a dictionary format.
    """
    from datetime import datetime
    now = datetime.now()
    return {
        "date_and_time": now.strftime("%Y-%m-%d %H:%M:%S"),
    }

# Fetch data from an external API
def get_randomuser_from_ramdomuserme() -> dict:
    """
    Returns a random user from randomuser.me API.
    Returns a dictionary with user's full name, email, and phone number.
    """
    import requests
    response = requests.get("https://randomuser.me/api/")
    if response.status_code == 200:
        user = response.json()
        user_info = user['results'][0]
        full_name = f"{user_info['name']['first']} {user_info['name']['last']}"
        email = user_info['email']
        phone = user_info['phone']
        return {
            "full_name": full_name,
            "email": email,
            "phone": phone
        }
    else:
        return {"error": "Failed to fetch data from randomuser.me"}


# Define the root agent with tools
root_agent = Agent(
    name="tools_agent",
    description="A tool-using agent to find information.",
    tools=[get_current_date_and_time, get_randomuser_from_ramdomuserme],
    model="gemini-2.0-flash",
    instruction="""
  You are a helpful assistant that can use the following tools:
  - get_current_date_and_time: Returns the current date and time.
  - get_randomuser_from_ramdomuserme: Returns a random user from randomuser.me API.
  """
)
