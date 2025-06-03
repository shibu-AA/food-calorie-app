# 食事カロリー判定
---

## 概要
---
食事画像をアップロードすることで、食事メニューを判別し、カロリーを表示するWebアプリです。

## 使用技術
---
| 技術         | 説明                                     |
|--------------|------------------------------------------|
| Python       | アプリケーションの主要言語              |
| PyTorch      | CNNモデルの構築と学習                   |
| ResNet18     | 転移学習用で使用                        |
| Streamlit    | Webアプリケーションのフレームワーク     |
| ngrok        | 外部公開用                              |
| FastAPI      | 推論モデルのAPI化（今後使用予定）       |
| SQLite       | メニューとカロリー情報のデータベース    |
| Food-101     | 学習用の画像データセット                |

## ファイル構成
---
| ファイル名   | 説明                                     |
|--------------|------------------------------------------|
| app.py       | アプリケーションの主要言語               |
| model.py      | CNNモデルの構築と学習                   |
| model_food101.pth | 転移学習用で使用                    |
| Food101_calorie.db| Webアプリケーションのフレームワーク |

## セットアップと実行方法
---

### Google Colab 上での実行手順

#### 必要なライブラリのインストール
```bash
!pip install streamlit==1.27.2 --quiet
!pip install pyngrok --upgrade --quiet
!pip install --upgrade protobuf==3.20.0
!pip install --upgrade streamlit
```

#### ライブラリのインポート
```bash
import streamlit as st
from pyngrok import ngrok
```

#### ngrokの認証トークンの設定
```bash
#ここにあなたのngrokを入力してください
!ngrok authtoken "ここに入力"
```

#### Streamlitアプリを起動
```bash
!streamlit run app.py &>/dev/null&
```

#### 公開URLを表示
```bash
ngrok.kill()
url = ngrok.connect(addr="8501")
print(url)
```