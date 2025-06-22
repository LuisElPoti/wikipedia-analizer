from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas.saved_article import SavedArticleResponse, SavedArticleCreate
from db.deps import get_db
from db.models import SavedArticle
import json

router = APIRouter()

@router.post("/saved_articles/", response_model=SavedArticleResponse)
def save_article(article: SavedArticleCreate, db: Session = Depends(get_db)):
    try:
        db_article = SavedArticle(
            title=article.title,
            url=article.url,
            summary=article.summary,
            top_words=json.dumps(article.top_words),
            sentiment=json.dumps(article.sentiment),
            named_entities=json.dumps(article.named_entities),
            note=article.note,
        )
        db.add(db_article)
        db.commit()
        db.refresh(db_article)
        return SavedArticleResponse(
            id=db_article.id,
            title=db_article.title,
            url=db_article.url,
            summary=db_article.summary,
            top_words=json.loads(db_article.top_words),
            sentiment=json.loads(db_article.sentiment),
            named_entities=json.loads(db_article.named_entities),
            note=db_article.note,
            created_at=db_article.created_at,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar artículo: {str(e)}")

@router.get("/saved_articles/", response_model=List[SavedArticleResponse])
def list_saved_articles(db: Session = Depends(get_db)):
    try:
        articles = db.query(SavedArticle).all()
        return [
            SavedArticleResponse(
                id=a.id,
                title=a.title,
                url=a.url,
                summary=a.summary,
                top_words=json.loads(a.top_words),
                sentiment=json.loads(a.sentiment),
                named_entities=json.loads(a.named_entities),
                note=a.note,
                created_at=a.created_at,
            )
            for a in articles
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar artículos: {str(e)}")
