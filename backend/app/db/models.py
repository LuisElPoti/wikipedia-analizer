from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, JSON, Interval
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# Esta clase define la estructura de la tabla "saved_articles" y su relación con "article_analyses"
class SavedArticle(Base):
    __tablename__ = "saved_articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    summary = Column(Text, nullable=False)
    note = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    analysis = relationship("ArticleAnalysis", back_populates="article", cascade="all, delete-orphan", uselist=False, passive_deletes=True)

# Esta clase define la estructura de la tabla "article_analyses" y su relación con "saved_articles"
class ArticleAnalysis(Base):
    __tablename__ = "article_analyses"

    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("saved_articles.id", ondelete="CASCADE"), nullable=False, unique=True)
    frequent_words = Column(JSON, nullable=False)
    sentiment = Column(String, nullable=False)
    topics = Column(JSON, nullable=False)
    complexity = Column(String, nullable=False)
    word_count = Column(Integer, nullable=False)
    sentences = Column(Integer, nullable=False)
    avg_words_per_sentence = Column(Float, nullable=False)
    estimated_reading_time = Column(Integer, nullable=False)
    key_insights = Column(JSON, nullable=False)

    article = relationship("SavedArticle", back_populates="analysis")