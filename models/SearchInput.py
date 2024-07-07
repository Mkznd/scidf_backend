from pydantic import BaseModel


class SearchInput(BaseModel):
    queries: list[str]
    top_k_per_source: int = 10
