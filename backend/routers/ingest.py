from fastapi import APIRouter, UploadFile, File, Form
from services.embedder import split_text, load_pdf, load_url
from services.retriever import add_documents, list_collections, delete_document
from datetime import datetime

router = APIRouter()

@router.post("/ingest")
async def ingest_text(
    text: str = Form(...),
    title: str = Form(...),
    collection_name: str = Form(default="algorithms"),
):
    chunks = split_text(text)
    metadata_list = [
        {
            "title": title,
            "source": "text_input",
            "collection": collection_name,
            "created_at": datetime.now().isoformat(),
            "chunk_index": i,
        }
        for i in range(len(chunks))
    ]
    count = add_documents(collection_name, chunks, metadata_list)
    return {
        "status": "success",
        "title": title,
        "collection": collection_name,
        "chunks_added": count,
    }

@router.post("/ingest/pdf")
async def ingest_pdf(
    file: UploadFile = File(...),
    title: str = Form(...),
    collection_name: str = Form(default="algorithms"),
):
    """PDFファイルからテキスト抽出→チャンク→保存"""
    file_bytes = await file.read()
    text = load_pdf(file_bytes)
    chunks = split_text(text)
    metadata_list = [
        {
            "title": title,
            "source": file.filename,
            "collection": collection_name,
            "created_at": datetime.now().isoformat(),
            "chunk_index": i,
        }
        for i in range(len(chunks))
    ]
    count = add_documents(collection_name, chunks, metadata_list)
    return {
        "status": "success",
        "title": title,
        "collection": collection_name,
        "chunks_added": count,
    }

@router.post("/ingest/url")
async def ingest_url(
    url: str = Form(...),
    title: str = Form(...),
    collection_name: str = Form(default="algorithms"),
):
    """URLからテキスト抽出→チャンク→保存"""
    text = load_url(url)
    chunks = split_text(text)
    metadata_list = [
        {
            "title": title,
            "source": url,
            "collection": collection_name,
            "created_at": datetime.now().isoformat(),
            "chunk_index": i,
        }
        for i in range(len(chunks))
    ]
    count = add_documents(collection_name, chunks, metadata_list)
    return {
        "status": "success",
        "title": title,
        "collection": collection_name,
        "chunks_added": count,
    }

@router.get("/collections")
async def get_collections():
    return {"collections": list_collections()}

@router.delete("/document")
async def remove_document(
    title: str,
    collection_name: str = "algorithms",
):
    count = delete_document(collection_name, title)
    return {
        "status": "success",
        "title": title,
        "chunks_deleted": count,
    }