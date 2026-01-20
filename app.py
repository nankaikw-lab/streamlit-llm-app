import os
import streamlit as st
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# .env を読む（ローカル用）
load_dotenv()

st.set_page_config(page_title="LLMアプリ（練習）", page_icon="🧠")

st.title("LLM切り替えアプリ")

st.write("""
これは練習用のアプリです。  
A/Bの切り替えによって、LLMの性格が変わります。

**使い方**
1. AかBを選ぶ  
2. 質問を書く  
3. 送信する
""")


# A/Bの説明
st.write("**A**：厳密アシスタント")
st.write("**B**：適当アシスタント")

# ラジオボタン
ab = st.radio("AかBを選んでください", ["A", "B"], horizontal=True)

# 質問入力
text = st.text_area("質問を書いてください", "日本の首都を教えてください。")

# 送信ボタン
btn = st.button("送信")

# ---- 関数（要件：入力テキスト＋ラジオ選択値 → 回答を返す）----
def ask_llm(input_text, expert_choice):
    # A/Bでシステムメッセージを変える（初心者っぽく if で分岐）
    if expert_choice == "A":
        system_text = "You are a strict assistant.Your tone is very strict and direct. Explain step-by-step in simple Japanese."
    else:
        system_text = "You are a careless and free-spirited assistant. Your tone is very casual and humorous. Feel free to make jokes in your answers in Japanese."

    # LLMを作る
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # メッセージを作る
    msgs = [
        SystemMessage(content=system_text),
        HumanMessage(content=input_text),
    ]

    # 実行して返す
    res = llm(msgs)
    return res.content


# ボタンが押されたら実行
if btn:
    if text.strip() == "":
        st.warning("質問が空です。")
    else:
        try:
            with st.spinner("AIに聞いています..."):
                ans = ask_llm(text, ab)

            st.write("----")
            st.subheader("回答")
            st.write(ans)

        except Exception as e:
            # エラー表示
            st.error("エラーが出ました。")
            st.write(e)

st.write("----")