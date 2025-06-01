# プロジェクト名

簡単な説明文（1～2行）

## 📌 概要

このプロジェクトは〇〇を目的とした□□アプリです。  
画像を入力すると、AIが食事メニューを判定しカロリーを表示します。

## 🚀 特徴

- 食事画像からメニューを予測（Food-101 + ResNet）
- SQLite DBでカロリー情報を表示
- StreamlitによるWeb UI
- ngrok対応でインターネット公開も可能

## 🛠️ 使用技術

- Python 3.x
- PyTorch
- Streamlit
- SQLite
- ngrok

## 📥 インストール

1. リポジトリをクローン：

    ```bash
    git clone https://github.com/あなたのユーザー名/プロジェクト名.git
    cd プロジェクト名
    ```

2. 必要なパッケージをインストール：

    ```bash
    pip install -r requirements.txt
    ```

3. `.env` ファイルを作成して `NGROK_TOKEN` を記述：

    ```env
    NGROK_TOKEN=あなたのトークン
    ```

## ▶️ 実行方法

```bash
streamlit run app.py
