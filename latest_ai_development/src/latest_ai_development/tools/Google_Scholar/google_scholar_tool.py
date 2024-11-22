from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from latest_ai_development.tools.Google_Scholar.google_scholar import fetch_and_display_publications


class GoogleScholarToolInput(BaseModel):
    """Input schema for GoogleScholarToolInput."""
    authorId: str = Field(..., description="Auther Id of User")

class GoogleScholarTool(BaseTool):
    name: str = "Google scholar data Collector"
    description: str = (
        "Gives data of a particular google scholar profile based on google scholar user ID"
    )
    args_schema: Type[BaseModel] = GoogleScholarToolInput

    def _run(self, authorId: str) -> str:
        # Implementation goes here
        return fetch_and_display_publications(authorId)
        # return "this is an example of a tool output, ignore it and move along."
