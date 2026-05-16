import os
from pinecone import Pinecone
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pathlib import Path
import fitz
import requests
from bs4 import BeautifulSoup

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

def split_text(text: str) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )
    return splitter.split_text(text)

def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Pinecone Inference APIでEmbeddingを生成する。
    ローカルにモデルをロードしないのでメモリを使わない。
    """
    embeddings = pc.inference.embed(
        model="multilingual-e5-large",
        inputs=texts,
        parameters={"input_type": "passage"},
    )
    return [e["values"] for e in embeddings]

def embed_query(text: str) -> list[float]:
    """
    検索クエリ用のEmbedding。input_typeがqueryになる。
    """
    embeddings = pc.inference.embed(
        model="multilingual-e5-large",
        inputs=[text],
        parameters={"input_type": "query"},
    )
    return embeddings[0]["values"]

def load_markdown(file_path: str) -> str:
    return Path(file_path).read_text(encoding="utf-8")

def load_pdf(file_bytes: bytes) -> str:
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def load_url(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    response = requests.get(url, timeout=10, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()
    return soup.get_text(separator="\n", strip=True)