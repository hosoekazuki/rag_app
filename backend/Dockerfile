# Docker Imageを作成するための設計図

# ベースイメージ：python 3.11の軽量版
# slim = 不要なパッケージを除いた軽量版
FROM python:3.11-slim

# コンテナ内の作業ディレクトリを設定
# この語のコマンドはすべてこのディレクトリ上で実行される
WORKDIR /app

# 依存関係ファイルだけ先にコピー
# ライブラリが変わらない限りキャッシュが効く（ビルド高速化）
COPY requirements.txt .

# ライブラリインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコピー
COPY . .

# FastAPIサーバーを構築
# host = 0.0.0.0: コンテナ外からアクセスできるようにする
# port = 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]