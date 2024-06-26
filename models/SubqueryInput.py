from pydantic import BaseModel


class SubqueryInput(BaseModel):
    query: str
