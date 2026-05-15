import streamlit as st
import requests

# バックエンドのURL（Docker Compose内ではサービス名で接続）
API_BASE = "http://backend:8000"

# ページ設定
st.set_page_config(page_title="RAG Study App", layout="wide")
st.title("📚 RAG Study App")

# サイドバー：設定
st.sidebar.header("設定")
api_key = st.sidebar.text_input("Gemini APIキー", type="password")

# サイドバー：Collection選択
try:
    res = requests.get(f"{API_BASE}/collections")
    collections = res.json().get("collections", [])
except:
    collections = []

if collections:
    selected_collection = st.sidebar.selectbox("Collection", collections)
else:
    selected_collection = st.sidebar.text_input("Collection名", value="algorithms")

# メイン画面：タブで機能を切り替え
tab_search, tab_register, tab_manage = st.tabs(["🔍 検索", "📝 登録", "📋 管理"])

# ========== 検索タブ ==========
with tab_search:
    st.header("学習内容を検索")
    query = st.text_input("質問を入力")

    if st.button("検索", key="search_btn"):
        if not api_key:
            st.error("サイドバーにGemini APIキーを入力してください")
        elif not query:
            st.warning("質問を入力してください")
        else:
            with st.spinner("検索中..."):
                try:
                    res = requests.get(
                        f"{API_BASE}/query",
                        params={
                            "q": query,
                            "collection_name": selected_collection,
                        },
                        headers={"x-api-key": api_key},
                    )
                    data = res.json()

                    # 回答表示
                    st.subheader("回答")
                    st.write(data["answer"])

                    # 参照元表示
                    st.subheader("参照元")
                    for source in data["sources"]:
                        st.write(f"- {source['title']} (chunk {source['chunk_index']})")

                except Exception as e:
                    st.error(f"エラーが発生しました: {e}")

# ========== 登録タブ ==========
with tab_register:
    st.header("コンテンツ登録")
    source_type = st.radio("入力ソース", ["テキスト", "PDF", "URL"])
    title = st.text_input("タイトル")

    if source_type == "テキスト":
        text = st.text_area("テキスト", height=200)
        if st.button("登録", key="register_text"):
            if not title or not text:
                st.warning("タイトルとテキストを入力してください")
            else:
                with st.spinner("登録中..."):
                    try:
                        res = requests.post(
                            f"{API_BASE}/ingest",
                            data={
                                "text": text,
                                "title": title,
                                "collection_name": selected_collection,
                            },
                        )
                        data = res.json()
                        st.success(f"登録完了：{data['chunks_added']}チャンク追加")
                    except Exception as e:
                        st.error(f"エラー: {e}")

    elif source_type == "PDF":
        uploaded_file = st.file_uploader("PDFファイルをアップロード", type=["pdf"])
        if st.button("登録", key="register_pdf"):
            if not title or not uploaded_file:
                st.warning("タイトルとPDFファイルを指定してください")
            else:
                with st.spinner("登録中..."):
                    try:
                        res = requests.post(
                            f"{API_BASE}/ingest/pdf",
                            data={
                                "title": title,
                                "collection_name": selected_collection,
                            },
                            files={"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")},
                        )
                        data = res.json()
                        st.success(f"登録完了：{data['chunks_added']}チャンク追加")
                    except Exception as e:
                        st.error(f"エラー: {e}")

    elif source_type == "URL":
        url = st.text_input("URL")
        if st.button("登録", key="register_url"):
            if not title or not url:
                st.warning("タイトルとURLを入力してください")
            else:
                with st.spinner("登録中..."):
                    try:
                        res = requests.post(
                            f"{API_BASE}/ingest/url",
                            data={
                                "url": url,
                                "title": title,
                                "collection_name": selected_collection,
                            },
                        )
                        data = res.json()
                        st.success(f"登録完了：{data['chunks_added']}チャンク追加")
                    except Exception as e:
                        st.error(f"エラー: {e}")
# ========== 管理タブ ==========
with tab_manage:
    st.header("コンテンツ管理")
    delete_title = st.text_input("削除するタイトル")

    if st.button("削除", key="delete_btn"):
        if not delete_title:
            st.warning("タイトルを入力してください")
        else:
            with st.spinner("削除中..."):
                try:
                    res = requests.delete(
                        f"{API_BASE}/document",
                        params={
                            "title": delete_title,
                            "collection_name": selected_collection,
                        },
                    )
                    data = res.json()
                    st.success(f"削除完了：{data['chunks_deleted']}チャンク削除")
                except Exception as e:
                    st.error(f"エラーが発生しました: {e}")