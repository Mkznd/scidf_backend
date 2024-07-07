from pydantic import BaseModel

from models.Highlight import Highlight


class SummaryResponse(BaseModel):
    summary: str
    highlights: list[Highlight]
