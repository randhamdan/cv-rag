import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/ask"

st.set_page_config(
    page_title="CV RAG Chat",
    layout="centered"
)

st.title("CV RAG Chat")
st.caption("Ask questions about candidates and CVs")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! Ask me anything about the candidates."
        }
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Type your question here...")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    try:
        response = requests.post(
            API_URL,
            json={"question": user_input}
        )

        data = response.json()
        assistant_reply = data.get("answer", "No response returned.")

    except Exception as e:
        assistant_reply = f"Connection error: {str(e)}"

    st.session_state.messages.append({
        "role": "assistant",
        "content": assistant_reply
    })

    st.rerun()

if st.button("Clear Chat"):
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Chat cleared. Start a new conversation!"
        }
    ]
    st.rerun()