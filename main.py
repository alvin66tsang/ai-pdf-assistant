import streamlit as st
import os
from langchain_core.messages import HumanMessage, AIMessage
from utils import qa_agent
from dotenv import load_dotenv

load_dotenv()

st.title("AI PDF Assistant")

with st.sidebar:
    openai_api_key = st.text_input("Enter your OpenAI API key", type="password", value=os.getenv("OPENAI_API_KEY"))
    st.markdown("[Get you API Key](https://platform.openai.com/api-keys)")

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

question = st.text_input("Ask a question about the PDF", disabled=not uploaded_file)

if uploaded_file and question and not openai_api_key:
    st.info("Enter your OpenAI API key")

if uploaded_file and question and openai_api_key:
    with st.spinner("Processing..."):
        response = qa_agent(
            chat_history=st.session_state.chat_history,
            uploaded_file=uploaded_file,
            question=question,
            openai_api_key=openai_api_key
        )

        st.session_state.chat_history.append(HumanMessage(content=question))
        st.session_state.chat_history.append(AIMessage(content=response))

        st.write("### Answer")
        st.write(response)

if "chat_history" in st.session_state:
    with st.expander("Chat History"):
        for i in range(0, len(st.session_state["chat_history"]), 2):
            human = st.session_state["chat_history"][i]
            ai = st.session_state["chat_history"][i+1]

            st.write(f"User: {human.content}")
            st.write(f"AI: {ai.content}")
            if i < len(st.session_state["chat_history"]) -2:
                st.divider()
