import os
import chromadb
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from docx import Document
import fitz  # PyMuPDF

class VectorDB:
    """Simple Chroma vector store for RAG"""

    def __init__(self, collection_name: str = "rag_documents"):
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        self.collection = self.client.get_or_create_collection(collection_name)
        print(f"✅ VectorDB initialized: {collection_name}")

    def _read_file(self, file_path: str) -> str:
        ext = os.path.splitext(file_path)[1].lower()
        text = ""
        if ext == ".pdf":
            with fitz.open(file_path) as doc:
                for p in doc: text += p.get_text()
        elif ext in [".docx", ".doc"]:
            doc = Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
        elif ext in [".txt", ".md"]:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
        return text.strip()

    def chunk_text(self, text: str, chunk_size=600, overlap=100) -> List[str]:
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
        return splitter.split_text(text)

    def add_documents(self, documents: List[Dict[str, Any]]):
        all_texts, all_ids = [], []
        for i, doc in enumerate(documents):
            text = self._read_file(doc["content"])
            chunks = self.chunk_text(text)
            for j, chunk in enumerate(chunks):
                all_texts.append(chunk)
                all_ids.append(f"{i}_{j}")
        embeddings = self.embedding_model.encode(all_texts).tolist()
        self.collection.add(ids=all_ids, embeddings=embeddings, documents=all_texts)
        print(f"✅ Added {len(all_texts)} text chunks")

    def search(self, query: str, n_results=3) -> Dict[str, Any]:
        q_emb = self.embedding_model.encode([query]).tolist()
        res = self.collection.query(query_embeddings=q_emb, n_results=n_results)
        if not res.get("documents"):
            return {"documents": []}
        return {"documents": res["documents"][0]}
