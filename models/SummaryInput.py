from pydantic import BaseModel


class SummaryInput(BaseModel):
    url: str
