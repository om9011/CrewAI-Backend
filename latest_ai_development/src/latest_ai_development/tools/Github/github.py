import requests
import os
from dotenv import load_dotenv
load_dotenv()
# Set your GitHub token here
TOKEN = os.getenv("GITHUB_TOKEN")  # Or replace with your token string
print(TOKEN)
# Define the GraphQL query
query = """
query($userName:String!) {
  user(login: $userName){
    contributionsCollection {
      contributionCalendar {
        totalContributions
      }
    }
  }
}
"""
# weeks {
#           contributionDays {
#             contributionCount
#             date
#           }
#         }

def retrieve_contribution_data(user_name):
    # Define the variables
    variables = {"userName": user_name}

    # Define the request body
    body = {
        "query": query,
        "variables": variables
    }

    # Make the API request
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }
    response = requests.post("https://api.github.com/graphql", json=body, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Query failed with status code {response.status_code}: {response.text}")


# Replace with the desired GitHub username
# username = "om-gujarathi"
# data = retrieve_contribution_data(username)

# Print contribution data
# print(data)
