from pydantic import BaseModel
from typing import List, Tuple


class ArticleResponse(BaseModel):
    title: str
    url: str
    summary: str
    analisis: dict
