import streamlit as st
import os
from rag_assistant import RAGAssistant

# ======================================
# Caching the RAG model (per mode)
# ======================================
@st.cache_resource
def load_rag(mode: str):
    return RAGAssistant(mode=mode)

# ======================================
# Title + Mode Toggle
# ======================================
st.title("🧪 Virtual Chemistry RAG Lab")
st.subheader("Mix elements in test tubes and see the reaction!")

mode = st.radio("Choose AI Mode:", ["Strict Mode (Verified Only)", "Creative Mode (Scientific Reasoning)"])
selected_mode = "strict" if "Strict" in mode else "creative"

rag = load_rag(selected_mode)

# ======================================
# Reactant Properties
# ======================================
reactant_properties = {
    "H₂": {"Color": "colorless gas", "Behavior": "flammable", "Note": "forms H₂O with O₂"},
    "O₂": {"Color": "colorless gas", "Behavior": "supports combustion", "Note": "essential for respiration"},
    "Na": {"Color": "silvery solid", "Behavior": "corrosive, reacts violently with water", "Note": "forms NaOH + H₂"},
    "HCl": {"Color": "colorless acid", "Behavior": "corrosive", "Note": "neutralizes with base"},
    "Zn": {"Color": "bluish-silver metal", "Behavior": "reacts with acids", "Note": "produces hydrogen gas"},
    "S": {"Color": "yellow solid", "Behavior": "burns with blue flame", "Note": "forms SO₂ on combustion"},
}

reactant_a = st.selectbox("Reactant A", list(reactant_properties.keys()))
reactant_b = st.selectbox("Reactant B", list(reactant_properties.keys()))

# ======================================
# Show properties under each reactant
# ======================================
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"**Color:** {reactant_properties[reactant_a]['Color']}")
    st.markdown(f"**Behavior:** {reactant_properties[reactant_a]['Behavior']}")
    st.markdown(f"**Note:** {reactant_properties[reactant_a]['Note']}")

with col2:
    st.markdown(f"**Color:** {reactant_properties[reactant_b]['Color']}")
    st.markdown(f"**Behavior:** {reactant_properties[reactant_b]['Behavior']}")
    st.markdown(f"**Note:** {reactant_properties[reactant_b]['Note']}")

# ======================================
# Virtual Test Tubes
# ======================================
st.markdown("### 🧫 Virtual Test Tubes")
color_map = {
    "H₂": "#66ccff", "O₂": "#99ccff", "Na": "#cccccc", "HCl": "#ff6666",
    "Zn": "#999999", "S": "#ffcc00", "Default": "#cccccc"
}
tube_html = f"""
<div style="display:flex;gap:20px;">
  <div style='background:{color_map.get(reactant_a, "#ccc")};width:80px;height:120px;
  border-radius:40px 40px 10px 10px;text-align:center;color:white;line-height:120px;font-weight:bold;'>{reactant_a}</div>
  <div style='background:{color_map.get(reactant_b, "#ccc")};width:80px;height:120px;
  border-radius:40px 40px 10px 10px;text-align:center;color:white;line-height:120px;font-weight:bold;'>{reactant_b}</div>
</div>
"""
st.markdown(tube_html, unsafe_allow_html=True)

# ======================================
# RAG Reaction Retrieval
# ======================================
reaction_query = f"{reactant_a} + {reactant_b}"
response = rag.invoke(f"Reaction between {reaction_query}")

st.markdown(f"### ⚗️ Reaction Analysis for: {reaction_query}")
if "No known reaction" not in response:
    st.success(response)
else:
    st.warning(response)

# ======================================
# Chatbot Section
# ======================================
st.markdown("---")
st.markdown("### 💬 Ask the Chemistry Assistant")
user_query = st.text_input("Ask about this reaction or related chemistry:")

if user_query:
    chat_response = rag.invoke(user_query)
    st.markdown(f"**Assistant:** {chat_response}")
