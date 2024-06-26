from pydantic import BaseModel


class SearchInput(BaseModel):
    queries: list[str]
