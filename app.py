# 以下を「app.py」に書き込み
import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image
from model import predict, load_model
from model import get_calorie_from_db


import torch
device = "cuda" if torch.cuda.is_available() else "cpu"
net = load_model("model_food101.pth", device=device)


st.sidebar.title("画像認識アプリ")
st.sidebar.write("オリジナルの画像認識モデルを使って何の画像かを判定します。")

st.sidebar.write("")

img_source = st.sidebar.radio("画像のソースを選択してください。",
                              ("画像をアップロード", "カメラで撮影"))
if img_source == "画像をアップロード":
    img_file = st.sidebar.file_uploader("画像を選択してください。", type=["png", "jpg", "jpeg"])
elif img_source == "カメラで撮影":
    img_file = st.camera_input("カメラで撮影")

if img_file is not None:
    with st.spinner("推定中..."):
        img = Image.open(img_file)
        st.image(img, caption="対象の画像", width=480)
        st.write("")

        # 予測
        results = predict(img, net, device=device)

        if not results:
            st.error("予測に失敗しました。画像が不明瞭か、未対応の食べ物の可能性があります。")
            st.stop()

        # 結果の表示
        st.subheader("判定結果")
        n_top = 3  # 確率が高い順に3位まで返す
        for result in results[:n_top]:
            st.write(str(round(result[1]*100, 2)) + "%の確率で" + result[0] + "です。")

        # 判定結果の表示
        st.subheader("判定結果（上位3件）")
        top_candidates = [result[0] for result in results[:n_top]]
        selected_food = st.radio("正しい食べ物を選択してください。", top_candidates)

        # ユーザーが選択した食べ物のカロリーを取得して表示
        if selected_food:
            kcal = get_calorie_from_db(selected_food)
            if kcal is not None:
                st.success(f"「{selected_food}」のカロリーは {kcal} kcal です。")
            else:
                st.error(f"「{selected_food}」のカロリー情報が見つかりませんでした。")


st.sidebar.write("")
st.sidebar.write("")

st.sidebar.caption("""
このアプリは、「Food-101」を訓練データとして使っています。
""")
