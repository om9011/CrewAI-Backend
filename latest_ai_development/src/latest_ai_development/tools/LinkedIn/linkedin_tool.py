from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from latest_ai_development.tools.LinkedIn.linkedin import fetch_linkedin_account


class LinkedInToolInput(BaseModel):
    """Input schema for LeetcodeToolInput."""
    username: str = Field(..., description="Username of a LinkedIn profile")

class LinkedInTool(BaseTool):
    name: str = "Linkedin data Collector"
    description: str = (
        "Gives data of posts ofparticular a linkedin profile based on username"
    )
    args_schema: Type[BaseModel] = LinkedInToolInput

    def _run(self, username: str) -> str:
        # Implementation goes here
        return fetch_linkedin_account(username)
