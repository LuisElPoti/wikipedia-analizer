from fastapi import APIRouter, HTTPException
from typing import List
from app.db.prisma_client import prisma
from app.schemas.saved_article import SavedArticleCreate, SavedArticleResponse
import json

router = APIRouter()

@router.post("/saved_articles/", response_model=SavedArticleResponse)
async def save_article(article: SavedArticleCreate):
    created = await prisma.savedarticle.create(
        data={
            "title": article.title,
            "url": article.url,
            "summary": article.summary,
            "topWords": json.dumps(article.top_words),  # Guarda como JSON string
            "sentiment": json.dumps(article.sentiment),
            "namedEntities": json.dumps(article.named_entities),
            "note": article.note
        }
    )
    return SavedArticleResponse(
        id=created.id,
        title=created.title,
        url=created.url,
        summary=created.summary,
        top_words=json.loads(created.topWords),
        sentiment=json.loads(created.sentiment),
        named_entities=json.loads(created.namedEntities),
        note=created.note,
        created_at=created.createdAt
    )

@router.get("/saved_articles/", response_model=List[SavedArticleResponse])
async def list_saved_articles():
    articles = await prisma.savedarticle.find_many()
    return [
        SavedArticleResponse(
            id=a.id,
            title=a.title,
            url=a.url,
            summary=a.summary,
            top_words=json.loads(a.topWords),  
            sentiment=json.loads(a.sentiment), 
            named_entities=json.loads(a.namedEntities),  
            note=a.note,
            created_at=a.createdAt
        ) for a in articles
    ]

@router.delete("/saved_articles/{article_id}")
async def delete_article(article_id: int):
    article = await prisma.savedarticle.find_unique(where={"id": article_id})
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    await prisma.savedarticle.delete(where={"id": article_id})
    return {"detail": "Article deleted"}
