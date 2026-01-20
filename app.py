import os
import streamlit as st
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

load_dotenv()

# -----------------------------
# A/B 専門家プロンプト定義
# -----------------------------
EXPERT_SYSTEM_PROMPTS = {
    "A": (
        "You are Expert A. "
        "You answer as a friendly travel guide specializing in Japan and Okinawa. "
        "Give practical and warm recommendations."
    ),
    "B": (
        "You are Expert B. "
        "You answer as a professional IT support engineer. "
        "Explain step-by-step in simple Japanese with clear solutions."
    ),
}


# -----------------------------
# 入力テキスト + ラジオ選択値 → LLM回答
# -----------------------------
def ask_llm(input_text: str, expert_choice: str) -> str:

    system_prompt = EXPERT_SYSTEM_PROMPTS[expert_choice]

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=input_text),
    ]

    result = llm(messages)
    return result.content


# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="A/B専門家LLMデモ", page_icon="🧠")

st.title("🧠 A/B 専門家切替 LLM デモ")

st.write(
"""
このアプリでは、**LLMの振る舞いを A / B の2種類で切り替え**できます。

### 専門家設定
- **A** : 日本・沖縄に詳しい旅行ガイド  
- **B** : ITサポートエンジニア  

### 使い方
1. A または B を選択  
2. 質問文を入力  
3. 送信ボタンを押す  
"""
)

expert_choice = st.radio(
    "専門家タイプを選択してください",
    options=["A", "B"],
    horizontal=True
)

input_text = st.text_area(
    "入力テキスト",
    value="日本の首都を教えてください。",
    height=120
)

send = st.button("送信", type="primary")

if send:
    if not input_text.strip():
        st.warning("入力テキストを入力してください。")
    else:
        with st.spinner("LLMが回答中..."):
            answer = ask_llm(input_text, expert_choice)

        st.subheader("回答")
        st.write(answer)

st.divider()
st.caption("※ .env に OPENAI_API_KEY を設定してから streamlit run app.py で起動してください")