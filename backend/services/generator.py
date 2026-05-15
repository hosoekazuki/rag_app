from google import genai

def generate_answer(query: str, contexts: list[str], api_key: str) -> str:
    """
    検索結果をもとにGemini APIで回答を生成する。
    
    query    : ユーザーの質問
    contexts : 検索でヒットしたチャンクのリスト
    api_key  : ユーザーが持ち込むGemini APIキー（BYOK）
    """
    # クライアント初期化（BYOKのためリクエストごとに作る）
    client = genai.Client(api_key=api_key)
    
    # 検索結果をプロンプトに組み込む
    context_text = "\n\n---\n\n".join(contexts)
    
    prompt = f"""あなたは学習内容を整理して教えるアシスタントです。
以下の参考資料をもとに、質問に日本語で回答してください。
参考資料にない情報は「資料にはありません」と答えてください。

## 参考資料
{context_text}

## 質問
{query}
"""
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    
    return response.text