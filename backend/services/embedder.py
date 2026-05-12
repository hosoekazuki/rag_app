from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from pathlib import Path

model = SentenceTransformer("all-MiniLM-L6-v2")

def split_text(text: str) -> list[str]:
    """
    テキストをチャンク分割
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap = 50,
    )
    return splitter.split_text(text)
def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    テキストのリストをEmbeddingに変換する
    戻り値：ベクトルのリスト
    """
    embeddings = model.encode(texts)
    return embeddings.tolist()
def load_markdown(file_path: str) -> str:
    """
    Markdownファイルを読み込んでテキストとして返す
    """
    return Path(file_path).read_text(encoding="utf-8")
