# 🧠 Virtual Chemistry RAG Lab 
Welcome to  **RAG Lab**-   An interactive Retrieval-Augmented Generation (RAG) application built with Streamlit, combining AI-assisted chemistry reasoning and a vector-based knowledge base.
Users can mix elements virtually, observe predicted reactions, and query a context-aware assistant that reasons using scientific text files stored locally.

---

## 🧪 Overview
## 🌟 Table of Contents

- [🔬 Overview](#-overview)
- [🗂 Repository Structure](#-repository-structure)
- [✨ Features](#-features)
- [💻 Installation Guide](#-installation-guide)
- [▶️ Running the App](#️-running-the-app)
- [🧠 Data & Knowledge Base](#-data--knowledge-base)
- [🧩 Prompt Template & RAG Workflow](#-prompt-template--rag-workflow)
- [🚀 Future Improvements](#-future-improvements)
- [📜 License](#-license)
- [🧪 Credits](#-credits)

---

## 🔬 Overview

The **Virtual Chemistry RAG Lab** simulates laboratory-style experiments in a conversational AI environment.  
It retrieves factual data from curated `.txt` chemistry documents and uses **Retrieval-Augmented Generation (RAG)** to answer questions like:

> 🧪 “What happens when Zinc reacts with Hydrochloric acid?”  
> ⚡ “Explain the oxidation process in simple terms.”

All responses are **explainable** and **scientifically contextualized** using embeddings stored in a local vector database.

---

## 🗂 Repository Structure

rag_lab/
│
├── data/ # Knowledge base of text files (e.g. reactions_knowledge.txt)
│
├── src/
│ ├── app_lab_chat.py # Streamlit user interface for the virtual lab
│ ├── rag_assistant.py # Core RAG logic integrating retrieval + generation
│ ├── vector_db.py # Vector store creation and similarity search
│ └── requirements.txt # All dependencies
│
└── README.md # You are here

yaml
Copy code

---

## ✨ Features

### 🧫 1. Virtual Chemistry Experimentation
- Choose two reactants from a dropdown (e.g., **Zn + HCl**, **H₂ + O₂**).  
- View realistic **test tubes with color-coded chemicals**.  
- Retrieve reaction details and safety notes from the AI assistant.

---

### ⚙️ 2. Retrieval-Augmented Generation (RAG)
- Uses a **local text knowledge base** (`data/*.txt`).  
- Texts embedded using **SentenceTransformer embeddings**.  
- Queries matched to **semantically similar** chunks.  
- Ensures **factual**, **context-aware**, and **explainable** responses.

---

### 💬 3. Chemistry-Aware Chatbot
Ask contextual questions such as:
- “What is this reaction?”
- “Is it safe to heat sodium?”
- “Explain oxidation in this experiment.”

The assistant answers based on **retrieved chemistry data** and **reasoned interpretation**.

---

### 🧠 4. Prompt Templates & Context Reasoning

Structured **prompt templates** control AI behavior and ensure reliability.

**System Prompt Example:**
You are a chemistry lab assistant.
Explain reactions in simple, factual, and educational terms using the retrieved context.

markdown
Copy code

**User Prompt Example:**
Reaction between Zn and HCl

yaml
Copy code

**This ensures:**
- ✅ Consistency across responses  
- ✅ Explainability (uses only retrieved verified text)  
- ✅ Educational clarity for learners

---

### 🧩 5. Vector Database Integration

The `vector_db.py` module:
- Reads `.txt` chemistry files  
- Converts them into **vector embeddings**  
- Stores them locally for fast similarity-based retrieval  

💡 **Benefits:**
- Works **offline**  
- Enables **semantic search** (beyond keyword matching)  
- Provides **faster, context-relevant lookups**

---

### 🔍 6. Knowledge Transparency
All `.txt` knowledge files (like `reactions_knowledge.txt`, `water_formation.txt`) are **human-readable**.  
Users can verify what the model "knows" — ensuring **trust**, **auditability**, and **educational transparency**.

---

## 💻 Installation Guide

### Step 1 — Clone the Repository
```bash
git clone https://github.com/Blessy456b/rag_lab.git
cd rag_lab/src
```
Step 2 — Create and Activate Virtual Environment
```bash
Copy code
# Create virtual environment
python3 -m venv rag_lab_env
```
# Activate (Linux/Mac)
```bash
source rag_lab_env/bin/activate


Step 3 — Install Dependencies
bash
Copy code
pip install -r requirements.txt
▶️ Running the App
🧠 Option 1 — Streamlit Interface
bash
Copy code
streamlit run app_lab_chat.py
⚙️ Option 2 — Command-Line Testing
bash
Copy code
python3 rag_assistant.py
Use this mode to test retrieval and response generation without a GUI.

🧠 Data & Knowledge Base
All domain knowledge is stored as .txt files under data/.

Examples:

reactions_knowledge.txt → Common chemical reactions

water_formation.txt → Oxidation and combustion

biotechnology.txt → (Optional) cross-domain test

These are automatically vectorized at runtime for retrieval and reasoning.

🧩 Prompt Template & RAG Workflow
🔁 Flow:
User enters query → “Reaction between Zn and O₂”

Query is embedded via a transformer model

Most relevant text chunks retrieved from data/*.txt

Retrieved content + user query → fed into a prompt

Model generates accurate, explainable answers

💡 Why It Matters:
Reduces AI hallucination

Keeps responses domain-grounded

Makes system adaptable to new subjects — simply swap .txt files!

🚀 Future Improvements
🌐 Multilingual chemistry support (Hindi, Marathi, etc.)

🧪 Reaction visualization with animations

📊 Store user experiment logs/history

🧬 Extend to Physics and Biology domains

📜 License
This project is licensed under the MIT License — free for academic, research, and educational use.

🧪 Credits
Developed by: Blessy Thomas
Built with ❤️ using Streamlit, LangChain, and Vector Search.

yaml
Copy code

