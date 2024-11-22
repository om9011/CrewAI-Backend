from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from latest_ai_development.tools.Leetcode.leetcode_graphql import retrieve_leetcode_data


class LeetcodeToolInput(BaseModel):
    """Input schema for LeetcodeToolInput."""
    username: str = Field(..., description="Username of a leetcode profile")

class LeetcodeTool(BaseTool):
    name: str = "Leetcode data Collector"
    description: str = (
        "Gives data of a particular leetcode profile based on username"
    )
    args_schema: Type[BaseModel] = LeetcodeToolInput

    def _run(self, username: str) -> str:
        # Implementation goes here
        return retrieve_leetcode_data(username)
