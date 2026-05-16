# RAG Study App

学習コンテンツを登録・検索できる RAG（Retrieval-Augmented Generation）アプリです。
テキスト・PDF・URLからドキュメントを取り込み、自然言語で質問すると Gemini が回答を生成します。

## 構成

```
rag_app/
├── backend/        # FastAPI（ポート 8000）
│   ├── main.py
│   ├── routers/
│   │   ├── ingest.py   # ドキュメント登録 API
│   │   └── query.py    # 検索・回答生成 API
│   └── services/
│       ├── embedder.py  # テキスト分割・埋め込み・PDF/URLロード
│       ├── retriever.py # Pinecone へのベクトル保存・検索
│       └── generator.py # Gemini による回答生成
└── frontend/       # Streamlit（ポート 8501）
    └── app.py
```

## 使い方

### 1. 環境変数の設定

`docker-compose.yml` の `PINECONE_API_KEY` を自分のキーに書き換えてください。

```yaml
environment:
  - PINECONE_API_KEY=your_pinecone_api_key
```

### 2. 起動

```bash
docker compose up --build
```

- フロントエンド: http://localhost:8501
- バックエンド（API）: http://localhost:8000

### 3. アプリの使い方

1. サイドバーに **Gemini API キー** を入力（BYOK 方式 — サーバーには保存されません）
2. **Collection** を選択または新規作成
3. **登録タブ** でテキスト・PDF・URL からコンテンツを登録
4. **検索タブ** で質問を入力して回答を取得
5. **管理タブ** で登録済みドキュメントの確認・削除

## 技術スタック

| レイヤー | 技術 |
|---|---|
| フロントエンド | Streamlit |
| バックエンド | FastAPI + Uvicorn |
| ベクトル DB | Pinecone（インデックス名: `ragapp`、Collection = namespace） |
| 埋め込みモデル | Pinecone Inference API（`multilingual-e5-large`、1024次元） |
| LLM | Gemini 2.5 Flash（BYOK） |
| コンテナ | Docker Compose |

## ローカル開発（Docker なし）

```bash
# バックエンド（backend/ 内で実行）
pip install -r requirements.txt
PINECONE_API_KEY=your_key uvicorn main:app --reload --port 8000

# フロントエンド（frontend/ 内で実行）
pip install -r requirements.txt
API_BASE_URL=http://localhost:8000 streamlit run app.py
```
