from fastapi import FastAPI
from api.routes import articles, saved_articles
from contextlib import asynccontextmanager
from db.models import Base
from db.session import engine
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Crear tablas al inicio
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Wikipedia Analyzer Backend")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

@app.get("/")
def root():
    return {"message": "Wikipedia backend funcionando correctamente", "version": "1.0"}

app.include_router(articles.router)
app.include_router(saved_articles.router)

#correr el servidor con uvicorn main:app --reload

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)