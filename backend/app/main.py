from fastapi import FastAPI
from app.api.routes import articles, saved_articles
from app.db.prisma_client import connect_prisma, disconnect_prisma
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_prisma()
    yield
    await disconnect_prisma()
    
app = FastAPI(title="Wikipedia Analyzer Backend", lifespan=lifespan)

@app.get("/")
def root():
    return {"message": "Wikipedia backend funcionando correctamente"}

app.include_router(articles.router)
app.include_router(saved_articles.router)



