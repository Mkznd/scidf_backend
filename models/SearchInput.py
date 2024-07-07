from pydantic import BaseModel


class SearchInput(BaseModel):
    research_topic: str
