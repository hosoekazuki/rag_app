from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from pathlib import Path
import fitz  # pymupdf
import requests
from bs4 import BeautifulSoup

model = SentenceTransformer("all-MiniLM-L6-v2")

def split_text(text: str) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )
    return splitter.split_text(text)

def embed_texts(texts: list[str]) -> list[list[float]]:
    embeddings = model.encode(texts)
    return embeddings.tolist()

def load_markdown(file_path: str) -> str:
    return Path(file_path).read_text(encoding="utf-8")

def load_pdf(file_bytes: bytes) -> str:
    """
    PDFのバイトデータからテキストを抽出する。
    ページごとにテキストを結合して返す。
    """
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def load_url(url: str) -> str:
    """
    URLからHTMLを取得し、本文テキストを抽出する。
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    response = requests.get(url, timeout=10, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()
    
    return soup.get_text(separator="\n", strip=True)