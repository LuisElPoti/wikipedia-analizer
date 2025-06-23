from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import List
from schemas.saved_article import SavedArticleResponse, SavedArticleCreate, ArticleAnalysis
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
            note=article.note,
        )
        db.add(db_article)
        db.commit()
        db.refresh(db_article)
        
        # 2. Guardar análisis relacionado
        analysis = article.analisis  # ← Esto debe venir dentro del payload del artículo
        db_analysis = ArticleAnalysis(
            article_id=db_article.id,
            frequent_words=analysis.frequent_words,
            sentiment=analysis.sentiment,
            topics=analysis.topics,
            complexity=analysis.complexity,
            word_count=analysis.word_count,
            sentences=analysis.sentences,
            avg_words_per_sentence=analysis.avg_words_per_sentence,
            estimated_reading_time=analysis.estimated_reading_time,
            key_insights=analysis.key_insights,
        )
        db.add(db_analysis)
        db.commit()

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


@router.delete("/saved_articles/{article_id}", status_code=204)
def delete_article(article_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    article = db.query(SavedArticle).filter(SavedArticle.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")
    db.delete(article)
    db.commit()
    return


# PUT /saved_articles/{article_id}
@router.put("/saved_articles/{article_id}", response_model=SavedArticleResponse)
def update_article(article_id: int, updated: SavedArticleCreate, db: Session = Depends(get_db)):
    article = db.query(SavedArticle).filter(SavedArticle.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")

    article.title = updated.title
    article.url = updated.url
    article.summary = updated.summary
    article.top_words = json.dumps(updated.top_words)
    article.sentiment = json.dumps(updated.sentiment)
    article.named_entities = json.dumps(updated.named_entities)
    article.note = updated.note

    db.commit()
    db.refresh(article)

    return SavedArticleResponse(
        id=article.id,
        title=article.title,
        url=article.url,
        summary=article.summary,
        top_words=json.loads(article.top_words),
        sentiment=json.loads(article.sentiment),
        named_entities=json.loads(article.named_entities),
        note=article.note,
        created_at=article.created_at,
    )