from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session, joinedload
from typing import List
from schemas.saved_article import SavedArticleResponse, SavedArticleCreate, ArticleAnalysis, SavedArticleUpdateNote
from db.deps import get_db
from db.models import SavedArticle, ArticleAnalysis
import json

router = APIRouter()

@router.post("/saved_articles/", response_model=SavedArticleResponse)
def save_article(article: SavedArticleCreate, db: Session = Depends(get_db)):
    """
    Guarda un artículo en la base de datos.
    El artículo debe venir con su análisis ya generado.
    """
    
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

        # Guardar análisis 
        analysis = article.analisis
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
        db.refresh(db_analysis)

        db_article.analysis = db_analysis  

        return db_article
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar artículo: {str(e)}")

@router.get("/saved_articles/", response_model=List[SavedArticleResponse])
def list_saved_articles(db: Session = Depends(get_db)):
    try:
        articles = db.query(SavedArticle).options(joinedload(SavedArticle.analysis)).all()
        response = []
        for a in articles:
            analysis = None
            if a.analysis:
                analysis = ArticleAnalysis(
                    article_id=a.analysis.article_id,
                    frequent_words=a.analysis.frequent_words,
                    sentiment=a.analysis.sentiment,
                    topics=a.analysis.topics,
                    complexity=a.analysis.complexity,
                    word_count=a.analysis.word_count,
                    sentences=a.analysis.sentences,
                    avg_words_per_sentence=a.analysis.avg_words_per_sentence,
                    estimated_reading_time=a.analysis.estimated_reading_time,
                    key_insights=a.analysis.key_insights,
                )

            response.append(
                SavedArticleResponse(
                    id=a.id,
                    title=a.title,
                    url=a.url,
                    summary=a.summary,
                    note=a.note,
                    created_at=a.created_at,
                    analisis=analysis,
                )
            )
        return response
       
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar artículos: {str(e)}")


@router.get("/saved_articles/{article_id}", response_model=SavedArticleResponse)
def get_article(article_id: int, db: Session = Depends(get_db)):
    article = (
        db.query(SavedArticle)
        .options(joinedload(SavedArticle.analysis))
        .filter(SavedArticle.id == article_id)
        .first()
    )
    if not article:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")

    analysis = None
    if article.analysis:
        analysis = ArticleAnalysis(
            article_id=article.analysis.article_id,
            frequent_words=article.analysis.frequent_words,
            sentiment=article.analysis.sentiment,
            topics=article.analysis.topics,
            complexity=article.analysis.complexity,
            word_count=article.analysis.word_count,
            sentences=article.analysis.sentences,
            avg_words_per_sentence=article.analysis.avg_words_per_sentence,
            estimated_reading_time=article.analysis.estimated_reading_time,
            key_insights=article.analysis.key_insights,
        )

    return SavedArticleResponse(
        id=article.id,
        title=article.title,
        url=article.url,
        summary=article.summary,
        note=article.note,
        created_at=article.created_at,
        analisis=analysis,
    )


@router.delete("/saved_articles/{article_id}")
def delete_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(SavedArticle).filter(SavedArticle.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")

    db.delete(article)
    db.commit()
    return {"message": "Artículo eliminado correctamente"}


@router.put("/saved_articles/{article_id}", response_model=SavedArticleResponse)
def update_article_note(article_id: int, updated: SavedArticleUpdateNote, db: Session = Depends(get_db)):
    article = db.query(SavedArticle).options(joinedload(SavedArticle.analysis)).filter(SavedArticle.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")

    # Solo actualiza la nota
    article.note = updated.note
    db.commit()
    db.refresh(article)

    # Construir el análisis si existe
    analysis = None
    if article.analysis:
        analysis = ArticleAnalysis(
            article_id=article.analysis.article_id,
            frequent_words=article.analysis.frequent_words,
            sentiment=article.analysis.sentiment,
            topics=article.analysis.topics,
            complexity=article.analysis.complexity,
            word_count=article.analysis.word_count,
            sentences=article.analysis.sentences,
            avg_words_per_sentence=article.analysis.avg_words_per_sentence,
            estimated_reading_time=article.analysis.estimated_reading_time,
            key_insights=article.analysis.key_insights,
        )

    return SavedArticleResponse(
        id=article.id,
        title=article.title,
        url=article.url,
        summary=article.summary,
        note=article.note,
        created_at=article.created_at,
        analisis=analysis,
    )
