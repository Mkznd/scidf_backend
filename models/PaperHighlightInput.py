from pydantic import BaseModel

from models.Highlight import Highlight


class PaperHighlightInput(BaseModel):
    url: str
    highlights: list[Highlight]
