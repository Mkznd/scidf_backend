from pydantic import BaseModel


class RefineInput(BaseModel):
    query: str
