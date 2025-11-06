# Chemixtry Chatbot - Lab for Chemical Reactions
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
├── data/                         # Knowledge base of text files (e.g. reactions_knowledge.txt)    
│
├── src/  
│  │   ├── app_lab_chat.py           # Streamlit user interface for the virtual lab  
│  │   ├── rag_assistant.py          # Core RAG logic integrating retrieval + generation  
│  │   ├── vector_db.py              # Vector store creation and similarity search  
│  │  └── requirements.txt          # All dependencies  
│
└── README.md                     # You are here  


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

#### 🧩 Prompt Template Design
The Virtual Chemistry RAG Lab employs a structured prompt-based reasoning framework embedded within the RAGAssistant class.
This design ensures that the language model operates under controlled scientific constraints, adapting its reasoning behavior according to the selected operational mode —** Strict or Creative.**

The prompt structure consists of two key components:

- System Prompt — Defines the assistant’s personality, safety rules, and factual boundaries.

- User Template — Dynamically injects the retrieved contextual text and user query during runtime.

##### 1️⃣ System Prompt (Strict Mode)
Used when the model must produce strictly factual responses derived only from the retrieved knowledge base.
You are ChemGPT, a Virtual Chemistry Lab Assistant that answers ONLY
based on the retrieved knowledge base context. This is STRICT mode.

Rules:

- NEVER hypothesize or guess missing reactions.
- NEVER reference unrelated reactions or analogies.
- If context lacks information, say exactly:
- "No known reaction found in current knowledge base."
- Refuse unsafe, illegal, or manipulative questions.
- Use concise scientific tone with markdown formatting.
- Remember: You are not generating — you are retrieving factual info only.

This configuration enforces retrieval integrity — the model is constrained to operate purely within the context of verified chemistry data.
It prevents hallucination and maintains scientific trustworthiness.

##### 2️⃣ System Prompt (Creative Mode)
Used when the model is allowed to perform guided reasoning or educational expansion beyond the retrieved text.
You are ChemGPT Creative Mode — a Chemistry Assistant that combines
the retrieved context with your general scientific knowledge.

Rules:

- Start from context if available.
- If missing, you MAY infer plausible scientific explanations.
- Label inferred parts clearly, e.g., "Based on known chemistry..."
- Always include safety notes and clear disclaimers.
- Keep the tone educational and accurate.
This configuration encourages exploratory reasoning while maintaining transparency — any inference is explicitly labeled, ensuring the distinction between factual and generated content.

##### 3️⃣ User Prompt Template
Both modes utilize a shared template that injects retrieved text and user query into the LLM input during inference:
Context:
{context}

User Question:
{question}
Answer:

This template ensures a consistent reasoning pipeline — the assistant always grounds its answers in retrieved context before generating a response.
User Prompt:
Reaction between Zn and HCl.
This ensures factuality, educational tone, and consistent structure across responses.

### Modes of Operation
#### 4.1 Retrieval Mode (Offline)

Uses only locally stored .txt documents.
Works entirely offline — suitable for educational institutions.
Ensures traceable and verifiable outputs (no hallucinations).
#### 4.2 Chat Mode (Interactive Q&A)

Leverages generative AI reasoning (LLM) for conceptual discussions.
Offers explanatory, exploratory, and creative chemistry interactions.
Enables contextual dialogue (“Why does heating sodium release light?”).

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

# Create virtual environment
python3 -m venv rag_lab_env
```
# Activate (Linux/Mac)
```bash
source rag_lab_env/bin/activate
```

Step 3 — Install Dependencies
```bash

pip install -r requirements.txt
```
Your assistant supports GROQ model backend

Step 4 — Provider Model Example Environment Variable  
🧠 Groq llama-3.1-8b-instant GROQ_API_KEY  
🔧 Create a .env file inside /src:  
```bash
nano .env
```
Add the following lines depending on which API you plan to use:
Example 1 — Using Groq
```bash
GROQ_API_KEY=your_groq_key_here
```
⚠️ Security Note:
Do not share .env files or commit them to GitHub.
Instead, include a .env_example file showing the required variable names without real values.

### ▶️ Running the App
🧠 Option 1 — Streamlit Interface
```bash

streamlit run app_lab_chat.py
```
⚙️ Option 2 — Command-Line Testing
```bash

python3 rag_assistant.py
```
Use this mode to test retrieval and response generation without a GUI.

### 🧠 Data & Knowledge Base
All domain knowledge is stored as .txt files under data/.

Examples:

- reactions_knowledge.txt → Common chemical reactions

- water_formation.txt → Oxidation and combustion

- biotechnology.txt → (Optional) cross-domain test

These are automatically vectorized at runtime for retrieval and reasoning.

### 🧩 Prompt Template & RAG Workflow
🔁 Flow:
- User enters query → “Reaction between Zn and O₂”

- Query is embedded via a transformer model

- Most relevant text chunks retrieved from data/*.txt

- Retrieved content + user query → fed into a prompt

- Model generates accurate, explainable answers

### 💡 Why It Matters:
- Reduces AI hallucination

- Keeps responses domain-grounded

- Makes system adaptable to new subjects — simply swap .txt files!

### 🚀 Future Improvements
- 🌐 Multilingual chemistry support (Hindi, Marathi, etc.)

- 🧪 Reaction visualization with animations

-  📊 Store user experiment logs/history

-  🧬 Extend to Physics and Biology domains

### 📜 License
This project is licensed under the MIT License — free for academic, research, and educational use.

### 🧪 Credits
Developed by: Blessy Thomas
Built with curioisity using Streamlit, LangChain, and Vector Search.
Reach out at blessy456bthomas@gmail.com


