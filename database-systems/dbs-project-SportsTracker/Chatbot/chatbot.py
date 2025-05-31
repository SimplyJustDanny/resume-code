import streamlit as st
import time
from llm.chatollama import ChatOllamaBot


st.title("Sports Tracker Exercise AI Assistant")
st.caption("Powered by Ollama 3.2")

bot = ChatOllamaBot(st.session_state.username)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Let's start chatting! 👇"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("I will do as you say, give me your command"):

    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)


    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        assistant_response = bot.chat(prompt)

        for chunk in assistant_response.split(" "):
            chunk = chunk.replace("\n", "  \n")
            full_response += chunk + " "
            time.sleep(0.05)

            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
