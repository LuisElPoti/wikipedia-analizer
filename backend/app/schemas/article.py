from pydantic import BaseModel
from typing import List, Tuple

class Sentiment(BaseModel):
    polarity: float
    subjectivity: float

class ArticleResponse(BaseModel):
    title: str
    summary: str
    top_words: List[str]
    sentiment: Sentiment
    named_entities: List[Tuple[str, str]]
