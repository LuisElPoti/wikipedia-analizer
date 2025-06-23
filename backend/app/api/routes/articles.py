from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from services.wikipedia_service import search_wikipedia, get_article_summary, get_full_article
from services.analysis_service import generate_article_analysis
from schemas.article import ArticleResponse


router = APIRouter()

@router.get("/search", response_model=List[dict])
def search_articles(q: str):
    try:
        results = search_wikipedia(q)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar artículos: {str(e)}")
    
@router.get("/article/{title}", response_model=ArticleResponse)
def get_article(title: str):
    try:
        article = get_full_article(title)
        print("pase el articulo")
        analisis = generate_article_analysis(article)
        print("pase el analisis")
        if not article:
            raise HTTPException(status_code=404, detail=f"Article '{title}' not found")
        
        summary_data = get_article_summary(title)
        url = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"
        print("pase el summary")
        if not summary_data:
            raise HTTPException(status_code=404, detail=f"Summary for article '{title}' not found")
        
        return {"title": title, "url": url, "analisis": analisis, "summary": summary_data}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Article '{title}' not found except")

