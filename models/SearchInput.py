from pydantic import BaseModel


class SearchInput(BaseModel):
    queries: list[str]
    article_no: int = 10
