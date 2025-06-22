from pydantic import BaseModel
from typing import List, Tuple, Optional, Dict, Any
from datetime import datetime

class SavedArticleCreate(BaseModel):
    title: str
    url: str
    summary: str
    top_words: List[str]
    sentiment: Dict[str, float]
    named_entities: List[Tuple[str, str]]
    note: Optional[str] = None

class SavedArticleResponse(SavedArticleCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True