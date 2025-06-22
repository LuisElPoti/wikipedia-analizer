from fastapi import APIRouter, Depends, HTTPException
from app.services.wikipedia_service import search_wikipedia, get_article_summary
from app.services.analysis_service import analyze_text, analyze_sentiment, extract_named_entities
from app.schemas.article import ArticleResponse

router = APIRouter()

@router.get("/search", response_model=list[dict])
def search_articles(q: str):
    try:
        results = search_wikipedia(q)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar artículos: {str(e)}")

@router.get("/articles/{title}", response_model=ArticleResponse)
def get_article_detail(title: str):
    try:
        summary_data = get_article_summary(title)
        summary = summary_data.get("extract", "")
        top_words = analyze_text(summary)
        sentiment = analyze_sentiment(summary)
        named_entities = extract_named_entities(summary)
        return ArticleResponse(title=title, summary=summary, top_words=top_words, sentiment=sentiment, named_entities=named_entities)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Article '{title}' not found")