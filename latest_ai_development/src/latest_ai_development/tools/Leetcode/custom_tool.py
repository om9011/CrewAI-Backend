from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from latest_ai_development.tools.Leetcode.leetcode_graphql import retrieve_leetcode_data


class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: str = Field(..., description="Username of a leetcode profile")

class MyCustomTool(BaseTool):
    name: str = "Leetcode data Collector"
    description: str = (
        "Gives data of a particular leetcode profile based on username"
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: str) -> str:
        # Implementation goes here
        return retrieve_leetcode_data(argument)
        # return "this is an example of a tool output, ignore it and move along."
