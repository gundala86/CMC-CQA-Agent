
import streamlit as st
from agent.reasoning_agent import ReasoningAgent
from agent.intent_extraction_agent import IntentExtractionAgent
from agent.knowledge_base_loader import KnowledgeBase

st.set_page_config(page_title="CMC CQA Reasoning Agent (Phase 6)", page_icon="🧠", layout="wide")
st.title("🤖 CMC CQA Reasoning Agent — Phase 6 (Natural Language AI)")

kb_path = "output/CQA_KnowledgeBase_Master.csv"
kb = KnowledgeBase(kb_path)
agent = ReasoningAgent(kb_path)
intent_agent = IntentExtractionAgent(kb.get_modalities(), kb.get_phases())

query = st.text_input("Ask anything CMC related:")

if query:
    with st.spinner("Thinking..."):
        modality, phase = intent_agent.extract(query)

        if not modality or not phase:
            st.warning("❌ Sorry — could not extract both modality and phase. Please try rephrasing your question.")
        else:
            full_query = f"{modality} {phase}"
            response = agent.generate_control_strategy(full_query)
            st.markdown(response)
