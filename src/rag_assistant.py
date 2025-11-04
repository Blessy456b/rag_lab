import os
import glob
from typing import List
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from vectordb import VectorDB
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()


def load_documents() -> List[dict]:
    """Load chemistry knowledge base documents from ../data."""
    data_dir = "../data"
    files = glob.glob(os.path.join(data_dir, "*"))
    docs = []
    for fpath in files:
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                docs.append({
                    "content": f.read(),
                    "metadata": {"source": os.path.basename(fpath)}
                })
        except Exception as e:
            print(f"⚠️ Could not read {fpath}: {e}")
    return docs


class RAGAssistant:
    """
    🧪 Virtual Chemistry Lab Assistant
    - Supports Strict and Creative modes
    """

    def __init__(self, mode="strict"):
        self.mode = mode.lower()
        self.llm = self._get_llm()
        self.vector_db = VectorDB()
        self.chain = self._build_chain()
        print(f"✅ Chemistry Assistant ready in {self.mode.title()} Mode.")

    def _get_llm(self):
        """Select available LLM."""
        if os.getenv("GROQ_API_KEY"):
            return ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model="llama-3.1-8b-instant")
        else:
            raise ValueError("❌ No API key found in environment variables.")

    def _build_chain(self):
        """Define system prompt for both modes."""

        if self.mode == "strict":
            system_prompt = (
                "You are ChemGPT, a Virtual Chemistry Lab Assistant that answers ONLY "
                "based on the retrieved knowledge base context. This is STRICT mode.\n\n"
                "Rules:\n"
                "- NEVER hypothesize or guess missing reactions.\n"
                "- NEVER reference unrelated reactions or analogies.\n"
                "- If context lacks information, say exactly:\n"
                "  'No known reaction found in current knowledge base.'\n"
                "- Refuse unsafe, illegal, or manipulative questions.\n"
                "- Use concise scientific tone with markdown formatting.\n\n"
                "Remember: You are not generating — you are retrieving factual info only."
            )
        else:
            system_prompt = (
                "You are ChemGPT Creative Mode — a Chemistry Assistant that combines "
                "the retrieved context with your general scientific knowledge.\n\n"
                "Rules:\n"
                "- Start from context if available.\n"
                "- If missing, you MAY infer plausible scientific explanations.\n"
                "- Label inferred parts clearly, e.g., 'Based on known chemistry...'\n"
                "- Always include safety notes and clear disclaimers.\n"
                "- Keep the tone educational and accurate."
            )

        user_template = (
            "Context:\n{context}\n\n"
            "User Question:\n{question}\n\n"
            "Answer:"
        )

        system_msg = SystemMessagePromptTemplate.from_template(system_prompt)
        user_msg = ChatPromptTemplate.from_template(user_template)
        full_prompt = ChatPromptTemplate.from_messages([system_msg, user_msg])
        return full_prompt | self.llm | StrOutputParser()

    def add_documents(self, docs: List[dict]):
        """Add documents to vector database."""
        self.vector_db.add_documents(docs)

    def invoke(self, question: str) -> str:
        """Search KB and return context-based answer."""
        results = self.vector_db.search(question)
        docs = results.get("documents", [])
        context = "\n\n".join([d for d in docs if len(d.strip()) > 20])

        # Strict mode: hard refusal if no strong context
        if self.mode == "strict" and not context:
            return "No known reaction found in current knowledge base."

        answer = self.chain.invoke({"context": context or "No context available", "question": question}).strip()

        # Guard against hallucination in strict mode
        if self.mode == "strict" and any(kw in answer.lower() for kw in [
            "however", "may", "likely", "suggests", "possibly"
        ]):
            return "No known reaction found in current knowledge base."

        return answer
