from langchain.vectorstores import FAISS
from langchain.memory import VectorStoreRetrieverMemory
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnableLambda, RunnablePassthrough
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class ChatBot:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        self.llm = HuggingFaceEndpoint(
            model="meta-llama/Llama-3.3-70B-Instruct",
            task="text-generation",
            temperature=0
        )
        self.model = ChatHuggingFace(llm=self.llm)

        self.memory_store = FAISS.from_texts([""], self.embeddings)

        self.retriever = self.memory_store.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 10, "fetch_k": 50, "lambda_mult": 0.5}
        )

        self.memory = VectorStoreRetrieverMemory(retriever=self.retriever)

        self.prompt_template = """
            You are a concise and knowledgeable AI assistant.
            Use the past conversation if it helps answer the query, otherwise ignore it.
            The more recent/last conversation is the one with the higher timestamp value.

            Conversation history:
            {history}

            User Query:
            {query}

            Your answer:
        """
        self.prompt = PromptTemplate(
            template=self.prompt_template,
            input_variables=["history", "query"]
        )

        self.parser = StrOutputParser()

        self.chain = self._make_chain()

    def _make_chain(self):
        """Create runnable chain with history + query."""
        def get_history(query: str):
            history_docs = self.memory.load_memory_variables({'input': query})
            return history_docs.get("history", "")

        parallel_chain = RunnableParallel({
            'history': RunnableLambda(get_history),
            'query': RunnablePassthrough()
        })
        return parallel_chain | self.prompt | self.model | self.parser


    def ask(self, query: str):
        timestamp = datetime.now().isoformat()
        answer = self.chain.invoke(query)
        
        # Save context in memory with timestamp
        self.memory.save_context(
            {"input": query, "timestamp": timestamp},
            {"output": answer}
        )
        
        # Add to FAISS for retrieval
        self.memory_store.add_texts([query + " " + answer])
        
        # Optionally store timestamp in your session history
        return answer

    def get_history(self, query: str):
        """Retrieve conversation history relevant to a query."""
        history_docs = self.memory.load_memory_variables({'input': query})
        return history_docs.get("history", "")
