# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the app

```bash
# Start both services (backend + frontend)
docker compose up --build

# Backend only (FastAPI on :8000)
docker compose up backend

# Frontend only (Streamlit on :8501)
docker compose up frontend
```

The frontend connects to the backend via `API_BASE_URL` env var (defaults to `http://backend:8000` inside Docker). For local development without Docker, set `API_BASE_URL=http://localhost:8000` and run each service directly:

```bash
# Backend (from backend/)
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Frontend (from frontend/)
pip install -r requirements.txt
streamlit run app.py
```

## Architecture overview

This is a RAG (Retrieval-Augmented Generation) study app with two services:

**Backend** (`backend/`) — FastAPI, port 8000
- `main.py`: Mounts two routers — `ingest` and `query`
- `routers/ingest.py`: `/ingest` (text), `/ingest/pdf`, `/ingest/url`, `/collections`, `/documents`, `/document` (DELETE)
- `routers/query.py`: `/query` — vector search then LLM answer generation
- `services/embedder.py`: Text splitting (`RecursiveCharacterTextSplitter`, 500 chars/50 overlap), embedding via Pinecone Inference API (`multilingual-e5-large`, 1024-dim), PDF parsing (`pymupdf`), URL scraping (`beautifulsoup4`)
- `services/retriever.py`: Pinecone index named `"ragapp"`. **Collections are Pinecone namespaces**, not separate indexes. Vector IDs are MD5 hashes of `{title}_{chunk_index}`.
- `services/generator.py`: Gemini 2.5 Flash answer generation. BYOK — the Gemini API key is passed per-request via the `x-api-key` HTTP header (not stored server-side)

**Frontend** (`frontend/app.py`) — Streamlit, port 8501
- Three tabs: Search (query + answer display), Register (text/PDF/URL ingestion), Manage (list + delete documents)
- User enters their Gemini API key in the sidebar; it's forwarded as the `x-api-key` header to `/query`

## Key environment variables

| Variable | Where | Notes |
|---|---|---|
| `PINECONE_API_KEY` | backend | Required. Set in docker-compose or as env var. |
| `API_BASE_URL` | frontend | Backend URL. Defaults to `http://backend:8000`. |

The Gemini API key is not an env var — it is entered by the user in the UI at runtime (BYOK pattern).

## Running the embedder test script

```bash
# From backend/
python test_embedder.py
```

This requires `PINECONE_API_KEY` to be set and a markdown file at `data/algorithms/binary_search.md`.
