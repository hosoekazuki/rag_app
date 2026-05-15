from fastapi import APIRouter, Query, Header
from services.retriever import search
from services.generator import generate_answer

router = APIRouter()

@router.get("/query")
async def query_rag(
    q: str = Query(..., description="検索クエリ"),
    collection_name: str = Query(default="algorithms"),
    n_results: int = Query(default=3),
    x_api_key: str = Header(..., description="Gemini APIキー"),
):
    """
    RAG検索→回答生成のエンドポイント。
    
    q               : ユーザーの質問
    collection_name : 検索対象のCollection
    n_results       : 取得するチャンク数
    x_api_key       : HTTPヘッダーでAPIキーを受け取る（BYOK）
    """
    # ① ChromaDBで類似検索
    results = search(collection_name, q, n_results)
    
    # 検索結果からドキュメント本文を取り出す
    contexts = results["documents"][0] if results["documents"] else []
    metadatas = results["metadatas"][0] if results["metadatas"] else []
    
    if not contexts:
        return {
            "answer": "関連するドキュメントが見つかりませんでした。",
            "sources": [],
        }
    
    # ② Gemini APIで回答生成
    answer = generate_answer(q, contexts, x_api_key)
    
    # ③ 参照元情報を整形
    sources = [
        {
            "title": meta.get("title", ""),
            "chunk_index": meta.get("chunk_index", 0),
        }
        for meta in metadatas
    ]
    
    return {
        "answer": answer,
        "sources": sources,
    }