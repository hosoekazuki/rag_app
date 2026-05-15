import chromadb
from services.embedder import embed_texts

# ChromaDBクライアントの初期化
# persist_directory : データの保存先（コンテナ内）
client = chromadb.PersistentClient(path="/app/chroma_data")

def get_or_create_collection(collection_name: str):
    """
    Collectionを取得。なければ新規作成。
    RDBでいうテーブルに相当する。
    """
    return client.get_or_create_collection(name=collection_name)

def add_documents(collection_name: str, chunks: list[str], metadata_list: list[dict]):
    """
    チャンクをEmbeddingに変換してChromaDBに保存する。
    
    chunks        : 分割されたテキストのリスト
    metadata_list : 各チャンクに付与するメタデータのリスト
    """
    collection = get_or_create_collection(collection_name)
    
    # Embeddingに変換
    embeddings = embed_texts(chunks)
    
    # 各チャンクにユニークなIDを振る
    ids = [f"{metadata_list[0]['title']}_{i}" for i in range(len(chunks))]
    
    # ChromaDBに保存
    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadata_list,
    )
    
    return len(chunks)

def search(collection_name: str, query: str, n_results: int = 3):
    """
    クエリに類似したドキュメントを検索する。
    
    query     : 検索クエリ（テキスト）
    n_results : 返す件数
    """
    collection = get_or_create_collection(collection_name)
    
    # クエリをEmbeddingに変換
    query_embedding = embed_texts([query])[0]
    
    # 類似検索
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
    )
    
    return results

def list_collections():
    """
    全Collectionの名前一覧を返す。
    """
    collections = client.list_collections()
    return [col.name for col in collections]

def delete_document(collection_name: str, title: str):
    """
    タイトルに一致するドキュメントを削除する。
    """
    collection = get_or_create_collection(collection_name)
    
    # タイトルでフィルタして該当IDを取得
    results = collection.get(
        where={"title": title}
    )
    
    if results["ids"]:
        collection.delete(ids=results["ids"])
        return len(results["ids"])
    return 0