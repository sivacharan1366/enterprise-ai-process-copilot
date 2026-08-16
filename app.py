import streamlit as st
from dotenv import load_dotenv

from src.llm import generate_response

load_dotenv()

st.set_page_config(
    page_title="Enterprise AI Process Copilot",
    page_icon="🤖",
)

st.title("🤖 Enterprise AI Process Copilot")
st.write("AI assistant for enterprise knowledge and business processes")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are an enterprise AI assistant. "
                "Be helpful and concise. "
                "Do not invent company policies or facts."
            ),
        }
    ]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.write(message["content"])

user_input = st.chat_input("Ask something...")

if user_input:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):

        try:
            with st.spinner("Thinking..."):
                answer = generate_response(
                    st.session_state.messages
                )

            st.write(answer)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                }
            )

        except Exception as e:
            st.error(f"Error: {e}")