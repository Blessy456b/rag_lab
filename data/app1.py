import streamlit as st
from rag_assistant import RAGAssistant
import os

# -----------------------
# Initialize RAG Assistant
# -----------------------
@st.cache_resource
def load_rag_assistant():
    return RAGAssistant()

rag = load_rag_assistant()

# -----------------------
# UI Setup
# -----------------------
st.set_page_config(page_title="🧪 Virtual Chemistry RAG Lab", page_icon="⚗️")
st.title("🧪 Virtual Chemistry RAG Lab")

st.sidebar.header("🔬 Reaction Setup")
st.sidebar.write("Select elements or compounds to test reactions.")

# Sample compounds
elements = [
    "H₂", "O₂", "C", "Fe", "Zn", "Na", "Cl₂", "HCl", "NaOH", "Cu", "S"
]

col1, col2 = st.columns(2)
reactant_a = col1.selectbox("Reactant A", elements)
reactant_b = col2.selectbox("Reactant B", elements)

# -----------------------
# Display Test Tubes
# -----------------------
def colored_tube(label, color):
    return f"""
    <div style='
        display:inline-block;
        background:{color};
        width:80px;
        height:120px;
        border-radius:40px 40px 10px 10px;
        margin:10px;
        text-align:center;
        line-height:120px;
        font-weight:bold;
        color:white;
        font-size:20px;
    '>{label}</div>
    """

colors = {
    "H₂": "#a4d8ff", "O₂": "#ff6666", "C": "#444", "Fe": "#a67c52",
    "Zn": "#ccc", "Na": "#88ccff", "Cl₂": "#a8e063", "HCl": "#d88",
    "NaOH": "#66ccaa", "Cu": "#d17f45", "S": "#ffdb58"
}

st.markdown(
    f"<div style='text-align:center;'>{colored_tube(reactant_a, colors[reactant_a])}{colored_tube(reactant_b, colors[reactant_b])}</div>",
    unsafe_allow_html=True
)

if st.button("⚗️ Mix Reactants"):
    with st.spinner("Mixing chemicals and analyzing reaction..."):
        query = f"What happens when {reactant_a} reacts with {reactant_b}?"
        answer = rag.invoke(query)
    st.success(f"**Reaction Analysis for:** {reactant_a} + {reactant_b}")
    st.write(answer)

st.markdown("---")

# -----------------------
# Chat Section
# -----------------------
st.header("💬 Ask the Chemistry RAG Assistant")
user_query = st.text_input("Ask about reactions, properties, or safety:")

if st.button("🔍 Ask"):
    with st.spinner("Thinking..."):
        response = rag.invoke(user_query)
    st.write(response)
