import os
from pathlib import Path
import streamlit as st
from rag_assistant import RAGAssistant

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="🧪 Virtual Chemistry RAG Lab",
    layout="centered",
    page_icon="🧪"
)

# ---------------------------
# REACTANT PROPERTIES DATABASE
# ---------------------------
REACTANT_INFO = {
    "H₂": {"color": "colorless gas", "behavior": "highly flammable", "note": "forms explosive mixture with air"},
    "O₂": {"color": "colorless gas", "behavior": "supports combustion", "note": "essential for respiration"},
    "Na": {"color": "silvery-white metal", "behavior": "reactive with water", "note": "corrosive and produces hydrogen"},
    "Cl₂": {"color": "greenish-yellow gas", "behavior": "toxic", "note": "forms salts with metals"},
    "Fe": {"color": "grayish metal", "behavior": "rusts in presence of oxygen and moisture", "note": "forms Fe₂O₃"},
    "HCl": {"color": "colorless acid", "behavior": "corrosive", "note": "reacts with metals to release hydrogen"},
    "Zn": {"color": "bluish-silver metal", "behavior": "reacts with acids", "note": "produces hydrogen gas"},
    "S": {"color": "yellow solid", "behavior": "burns with blue flame", "note": "forms SO₂ on combustion"},
    "Cu": {"color": "reddish metal", "behavior": "forms black CuS with sulfur", "note": "used in electrical wiring"},
    "NaOH": {"color": "white solid", "behavior": "strong base", "note": "neutralizes acids to form salt + water"},
}

# ---------------------------
# LOAD RAG ASSISTANT (CACHED)
# ---------------------------
@st.cache_resource
def load_rag():
    rag = RAGAssistant()
    data_dir = Path("../data")
    docs = [{"content": str(f), "metadata": {"source": f.name}} for f in data_dir.glob("*.txt")]
    rag.add_documents(docs)
    return rag

rag = load_rag()

# ---------------------------
# FRONTEND UI
# ---------------------------
st.title("🧪 Virtual Chemistry RAG Lab")
st.markdown("Mix elements in test tubes and see the reaction!")

col1, col2 = st.columns(2)
with col1:
    reactant_a = st.selectbox("Reactant A", list(REACTANT_INFO.keys()), index=0)
    info_a = REACTANT_INFO[reactant_a]
    st.markdown(f"**Color:** {info_a['color']}  \n**Behavior:** {info_a['behavior']}  \n**Note:** {info_a['note']}")

with col2:
    reactant_b = st.selectbox("Reactant B", list(REACTANT_INFO.keys()), index=1)
    info_b = REACTANT_INFO[reactant_b]
    st.markdown(f"**Color:** {info_b['color']}  \n**Behavior:** {info_b['behavior']}  \n**Note:** {info_b['note']}")

# ---------------------------
# TEST TUBE VISUALIZATION
# ---------------------------
st.markdown("---")
st.markdown("### 🧫 Virtual Test Tubes")

tube_style = """
<style>
.testtube {
    display:inline-block;
    width:80px;
    height:150px;
    border-radius:40px 40px 10px 10px;
    margin:20px;
    text-align:center;
    line-height:150px;
    color:white;
    font-weight:bold;
    font-size:20px;
    transition:all 0.5s ease;
}
.blue { background:#4b9cd3; }
.red { background:#ff6666; }
.yellow { background:#f5c542; }
.green { background:#4CAF50; }
</style>
"""

st.markdown(tube_style, unsafe_allow_html=True)
color_map = {
    "H₂": "blue", "O₂": "red", "Na": "yellow", "Cl₂": "green",
    "Fe": "gray", "Zn": "yellow", "S": "yellow", "Cu": "orange",
    "NaOH": "green", "HCl": "red"
}

color_a = color_map.get(reactant_a, "blue")
color_b = color_map.get(reactant_b, "red")

st.markdown(
    f"<div class='testtube {color_a}'>{reactant_a}</div>"
    f"<div class='testtube {color_b}'>{reactant_b}</div>",
    unsafe_allow_html=True
)

# ---------------------------
# REACTION ANALYSIS
# ---------------------------
st.markdown("---")
st.markdown(f"### ⚗️ Reaction Analysis for: **{reactant_a} + {reactant_b}**")

reaction_query = f"{reactant_a} + {reactant_b}"
reaction_result = rag.invoke(reaction_query)

if "I don’t know" in reaction_result:
    st.warning("No known reaction found in current knowledge base.")
else:
    st.success(f"✅ Reaction Found: {reaction_result}")

# ---------------------------
# KNOWLEDGE BASE VIEWER
# ---------------------------
with st.expander("📚 View Knowledge Base Files"):
    for f in sorted(Path("../data").glob("*.txt")):
        st.markdown(f"- {f.name}")

# ---------------------------
# REACTION CHATBOT SECTION
# ---------------------------
st.markdown("---")
st.markdown("### 💬 Ask the Chemistry Assistant")
user_question = st.text_input("Ask about the reaction or related topics:")

if user_question:
    answer = rag.invoke(user_question)
    st.markdown(f"**Assistant:** {answer}")

