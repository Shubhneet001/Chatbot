import streamlit as st
from utils import ChatBot

# Streamlit setup
st.set_page_config(page_title="AI Chatbot", layout="centered")
st.title("AI Q&A Bot")

# Initialize ChatBot class
if "chatbot" not in st.session_state:
    st.session_state["chatbot"] = ChatBot()

chatbot = st.session_state["chatbot"]

# Session messages
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display previous chat
for msg in st.session_state["messages"]:
    st.chat_message("user").write(msg["user"])
    st.chat_message("assistant").write(msg["bot"])

# Chat input
query = st.chat_input("Ask anything")

if query:
    with st.spinner("Thinking..."):
        answer = chatbot.ask(query)
    st.session_state["messages"].append({"user": query, "bot": answer})
    st.chat_message("user").write(query)
    st.chat_message("assistant").write(answer)

# Sidebar reset button
st.sidebar.header("Options")
if st.sidebar.button("Reset Chat"):
    st.session_state["messages"] = []
    st.session_state["chatbot"] = ChatBot()
    st.success("Chat reset! Memory cleared.")
