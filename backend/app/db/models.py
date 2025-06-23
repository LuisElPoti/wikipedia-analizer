from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, JSON, Interval
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SavedArticle(Base):
    __tablename__ = "saved_articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    summary = Column(Text, nullable=False)
    note = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

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

    article = relationship("SavedArticle", backref="analysis", uselist=False)