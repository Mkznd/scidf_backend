from pydantic import BaseModel


class Highlight(BaseModel):
    type: str
    excerpt: str
    takeaway: str
    category: str
    woah_factor: int
