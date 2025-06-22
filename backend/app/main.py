from fastapi import FastAPI
from api.routes import articles, saved_articles
from contextlib import asynccontextmanager
from db.models import Base
from db.session import engine  # SQLAlchemy engine
import uvicorn

# Crear tablas al inicio
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Wikipedia Analyzer Backend")

@app.get("/")
def root():
    return {"message": "Wikipedia backend funcionando correctamente"}

app.include_router(articles.router)
app.include_router(saved_articles.router)

#correr el servidor con uvicorn main:app --reloa

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)