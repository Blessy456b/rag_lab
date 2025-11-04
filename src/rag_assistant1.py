import os, glob
from typing import List
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from vector_db import VectorDB
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

def load_documents() -> List[dict]:
    data_dir = "../data"
    files = glob.glob(os.path.join(data_dir, "*"))
    return [{"content": f, "metadata": {"source": os.path.basename(f)}} for f in files]

class RAGAssistant:
    def __init__(self):
        self.llm = self._get_llm()
        self.vector_db = VectorDB()
        template = (
            "You are a chemistry assistant that ONLY answers using the given context.\n"
            "If the reaction is unknown, say exactly:\n"
            "\"No known reaction found in current knowledge base.\"\n\n"
            "Context:\n{context}\n\nQuestion:\n{question}\nAnswer:"
        )
        self.chain = ChatPromptTemplate.from_template(template) | self.llm | StrOutputParser()
        print("✅ RAGAssistant ready.")

    def _get_llm(self):
        if os.getenv("GROQ_API_KEY"):
            return ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model="llama-3.1-8b-instant")
        elif os.getenv("OPENAI_API_KEY"):
            return ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o-mini")
        elif os.getenv("GOOGLE_API_KEY"):
            return ChatGoogleGenerativeAI(google_api_key=os.getenv("GOOGLE_API_KEY"), model="gemini-pro")
        else:
            raise ValueError("No API key found.")

    def add_documents(self, docs: List[dict]): self.vector_db.add_documents(docs)

    def invoke(self, question: str) -> str:
        results = self.vector_db.search(question)
        docs = results["documents"]
        if not docs: return "No known reaction found in current knowledge base."
        context = "\n\n".join(docs)
        return self.chain.invoke({"context": context, "question": question})


