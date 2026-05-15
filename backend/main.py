from fastapi import FastAPI
from routers.ingest import router as ingest_router
from routers.query import router as query_router

app = FastAPI()

app.include_router(ingest_router)
app.include_router(query_router)

@app.get("/")
def root():
    return {"message": "RAG Study App is running"}

@app.get("/health")
def health():
    return {"status": "ok"}