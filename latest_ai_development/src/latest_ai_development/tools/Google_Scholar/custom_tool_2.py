from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from latest_ai_development.tools.google_scholar import fetch_and_display_publications


class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: str = Field(..., description="Auther Id of User")

class MyCustomTool(BaseTool):
    name: str = "Research paper data Collector"
    description: str = (
        "Gives data of a particular google scholar profile based on author ID"
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: str) -> str:
        # Implementation goes here
        return fetch_and_display_publications(argument)
        # return "this is an example of a tool output, ignore it and move along."
