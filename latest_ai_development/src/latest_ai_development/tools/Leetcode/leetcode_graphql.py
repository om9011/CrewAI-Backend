import requests

# Define the GraphQL query for LeetCode
query = """
query($username: String!, , $year: Int) {
  matchedUser(username: $username) {
    username
    submitStats: submitStatsGlobal {
      acSubmissionNum {
        difficulty
        count
      }
    }
    profile {
      ranking
    }
    userCalendar(year: $year) {
      activeYears
    }
    languageProblemCount {
      languageName
      problemsSolved
    }
    tagProblemCounts {
      advanced {
        tagName
        problemsSolved
      }
      intermediate {
        tagName
        problemsSolved
      }
      fundamental {
        tagName
        problemsSolved
      }
    }
  }
  userContestRanking(username: $username) {
    attendedContestsCount
    topPercentage
  }
}
"""

def retrieve_leetcode_data(username):
    # Define the variables
    variables = {"username": username, "year": 2024}

    # Define the request body
    body = {
        "query": query,
        "variables": variables
    }

    # Make the API request (LeetCode does not require a token for basic queries)
    headers = {
        "Content-Type": "application/json",
        "Referer": "https://leetcode.com"
    }
    response = requests.post("https://leetcode.com/graphql", json=body, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Query failed with status code {response.status_code}: {response.text}")
