from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from latest_ai_development.tools.Github.github import retrieve_contribution_data


class GithubToolInput(BaseModel):
    """Input schema for GithubToolInput."""
    username: str = Field(..., description="Username of a github profile")

class GithubTool(BaseTool):
    name: str = "Github data Collector"
    description: str = (
        "Gives total contribution data of a particular github profile based on username"
    )
    args_schema: Type[BaseModel] = GithubToolInput

    def _run(self, username: str) -> str:
        # Implementation goes here
        return retrieve_contribution_data(username)
