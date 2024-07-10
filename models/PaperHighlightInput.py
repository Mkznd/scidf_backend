from pydantic import BaseModel


class PaperHighlightInput(BaseModel):
    url: str
    highlights: list[str]
