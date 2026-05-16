import os
from pinecone import Pinecone
from services.embedder import embed_texts

# Pineconeクライアント初期化
# 環境変数からAPIキーを取得
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("ragapp")

def add_documents(collection_name: str, chunks: list[str], metadata_list: list[dict]):
    """
    チャンクをEmbeddingに変換してPineconeに保存する。
    collection_name はnamespaceとして使う。
    """
    embeddings = embed_texts(chunks)
    
    vectors = []
    for i, (chunk, embedding, metadata) in enumerate(zip(chunks, embeddings, metadata_list)):
        import hashlib
        vec_id = hashlib.md5(f"{metadata['title']}_{i}".encode()).hexdigest()
        metadata["text"] = chunk
        vectors.append({
            "id": vec_id,
            "values": embedding,
            "metadata": metadata,
        })
    
    # namespaceでCollectionを分離
    index.upsert(vectors=vectors, namespace=collection_name)
    return len(chunks)

def search(collection_name: str, query: str, n_results: int = 3):
    """
    クエリに類似したドキュメントを検索する。
    """
    query_embedding = embed_texts([query])[0]
    
    results = index.query(
        vector=query_embedding,
        top_k=n_results,
        include_metadata=True,
        namespace=collection_name,
    )
    
    # ChromaDBと同じ形式で返す（query.pyを変更しなくて済む）
    documents = []
    metadatas = []
    for match in results["matches"]:
        documents.append(match["metadata"].get("text", ""))
        metadatas.append(match["metadata"])
    
    return {
        "documents": [documents],
        "metadatas": [metadatas],
    }

def list_collections():
    """
    全namespaceの一覧を返す。
    """
    stats = index.describe_index_stats()
    namespaces = list(stats.get("namespaces", {}).keys())
    return namespaces

def delete_document(collection_name: str, title: str):
    """
    タイトルに一致するドキュメントを削除する。
    """
    # Pineconeはメタデータでフィルタ削除できる
    results = index.query(
        vector=[0.0] * 384,  # ダミーベクトル
        top_k=100,
        include_metadata=True,
        namespace=collection_name,
        filter={"title": {"$eq": title}},
    )
    
    ids_to_delete = [match["id"] for match in results["matches"]]
    if ids_to_delete:
        index.delete(ids=ids_to_delete, namespace=collection_name)
    return len(ids_to_delete)

def get_or_create_collection(collection_name: str):
    """
    Pineconeではnamespaceが自動作成されるので何もしない。
    ingest.pyのdocuments APIとの互換用。
    """
    return None