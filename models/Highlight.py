from pydantic import BaseModel


class Highlight(BaseModel):
    excerpt: str
    takeaway: str
