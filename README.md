# My Journey throughout the project
*not generated with AI*

## 1. I made an AI chatbot:
- Using LangChain.
- Used Meta LLaMA model through Hugging Face API.
- Implemented memory of the chatbot using the FAISS vector store.
- Used MMR retriever.

## 2. Challenges I faced:
- My biggest challenge was to retrieve the relevant documents from the vector store (memory).
- This step was crucial as the chatbot works fine on short conversations with default retrievers but for long conversations we need to retrieve only the relevant and the recent conversations.
- I tried making different kinds of retrievers like:
  - **Dynamic retriever** that could adjust the number of documents to be retrieved according to the need (*it didn't work as it ignored the recency of the conversation*).
  - **Hybrid retriever** that could fetch the relevant docs + the recent conversation (*this gave many errors until I gave up on this*).
  - Finally, the **MMR retriever with timestamp** mentioned along with the conversation docs (*it works in most of the cases*).

## 3. Still the chatbot isn't perfect (some improvements I can make in the future):
- It sometimes hallucinates if the query contains only pronouns regarding the past conversations (**e.g**., *query: "explain it." -> gets confused which previous conversation to explain even though I have added timestamp*).
- I can also save the history locally so that I don't lose the history context on refreshing the webpage.


# AI Chatbot Project
*generated with AI*

## Project Overview
This project implements a **conversational AI chatbot** using **LangChain** with **Meta LLaMA** through the **Hugging Face API**.  
The chatbot maintains conversation memory using a **FAISS vector store** and retrieves relevant past conversation documents using **MMR (Maximal Marginal Relevance)** retrieval.  

---

## Features
- **Conversational AI** capable of answering user queries.
- **Persistent in-memory conversation memory** using FAISS.
- **Relevant context retrieval** with MMR retriever.
- **Prompt template** to maintain concise and informative responses.
- **Streamlit-based web interface** with chat history display.

---

## Challenges Faced
1. **Retrieving relevant documents from memory**
   - Works fine for short conversations, but long conversations require relevance + recency filtering.
2. **Different retrievers tried**
   - **Dynamic retriever:** Adjusts number of documents dynamically (ignored recency)
   - **Hybrid retriever:** Fetches relevant + recent conversations (caused errors)
   - **MMR retriever with timestamps:** Works in most cases
3. **Limitations**
   - The chatbot sometimes **hallucinates** if a query contains only pronouns referencing past conversation, e.g., `query: "explain it."`
   - History is currently in-memory, so it is lost on page refresh. Future improvements can include **saving history locally**.

---

## Project Workflow
1. **Setup**
   - Initialize **embedding model** (`HuggingFaceEmbeddings`).
   - Initialize **LLM** (`HuggingFaceEndpoint`) and **chat model** (`ChatHuggingFace`).
   - Create **FAISS vector store** for storing conversation memory.
   - Create **MMR retriever** for retrieving relevant documents from memory.

2. **Conversation Handling**
   - When a user asks a query:
     1. Retrieve relevant documents from memory using **MMR retriever**.
     2. Construct the **prompt template** using conversation history + user query.
     3. Pass prompt to the **chat model** for generating a response.
     4. Save the query and response in **memory store** for future retrieval.

3. **Streamlit App**
   - User interacts via **chat interface**.
   - Messages are stored in **session state**.
   - Option to **reset chat** clears memory (in RAM) and chat history.

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/Shubhneet001/Chatbot.git
cd my_chatbot
````

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set environment variables

Create a `.env` file in the project root:

```env
HF_TOKEN=hf_api_key
```


### 4. Run the Streamlit app

```bash
streamlit run app.py
```

### 5. Using the app

* Type your query in the chat box.
* Chatbot will respond using previous conversation context.
* Use **Reset Chat** button in the sidebar to clear conversation memory.

---

## Future Improvements

* Handle queries with pronouns better by improving context understanding.
* Save conversation history locally to persist memory across sessions.
* Add **recency-aware ranking** for MMR to always prioritize recent conversations.
* Optionally, integrate smaller models or APIs for faster response times.

---

## Requirements

* Python 3.10+
* `langchain`
* `langchain-huggingface`
* `faiss-cpu`
* `streamlit`
* `python-dotenv`

---
