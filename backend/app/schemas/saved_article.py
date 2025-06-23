from pydantic import BaseModel
from typing import List, Tuple, Optional, Dict, Any
from datetime import datetime

class ArticleAnalysis(BaseModel):
    article_id: int
    frequent_words: List[str]
    sentiment: str
    topics: List[str]
    complexity: str
    word_count: int
    sentences: int
    avg_words_per_sentence: float
    estimated_reading_time: int
    key_insights: List[str]

    class Config:
        from_attributes = True
        
class ArticleAnalysisCreate(BaseModel):
    frequent_words: List[str]
    sentiment: str
    topics: List[str]
    complexity: str
    word_count: int
    sentences: int
    avg_words_per_sentence: float
    estimated_reading_time: int  # en minutos
    key_insights: List[str]
        
class SavedArticleCreate(BaseModel):
    title: str
    url: str
    summary: str
    analisis: ArticleAnalysisCreate 
    note: Optional[str] = None
    

class SavedArticleUpdateNote(BaseModel):
    note: str
    
class SavedArticleResponse(SavedArticleCreate):
    id: int
    created_at: datetime
    analisis: Optional[ArticleAnalysis] = None

    class Config:
        from_attributes = True
        
