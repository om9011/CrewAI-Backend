from linkedin_api import Linkedin
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Authenticate using LinkedIn credentials
LINKEDIN_USERNAME = os.getenv("LINKEDIN_USERNAME")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")

api = Linkedin(LINKEDIN_USERNAME, LINKEDIN_PASSWORD)


def fetch_linkedin_account(username):
    try:
        print(f"Fetching data for user: {username}")

        # Fetch the latest posts
        posts = api.get_profile_posts(username, post_count=3)
        post_dict = {}

        for i, post in enumerate(posts):
            if post.get('commentary') and post['commentary'].get('text'):
                post_dict[f"Post {i + 1}"] =  post['commentary']['text']['text']
            else:
                post_dict[f"Post {i + 1}"] =  "No text content found in the post."

        # Return posts for scoring
        return post_dict
    except Exception as e:
        print(f"Error fetching LinkedIn data: {e}")
        return {}


# print(fetch_linkedin_account("omgujarathi"))