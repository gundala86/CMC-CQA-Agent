
import streamlit as st
from reasoning_agent import ReasoningAgent

st.set_page_config(page_title="CMC Reasoning Agent", page_icon="🧬", layout="wide")
st.title("🤖 CMC Reasoning Agent (Phase 4 - Control Strategy Generator)")

kb_path = "output/CQA_KnowledgeBase_Master.csv"
agent = ReasoningAgent(kb_path)

query = st.text_input("Ask for control strategy (ex: 'ADC Phase 1')")

if query:
    with st.spinner("Analyzing..."):
        response = agent.generate_control_strategy(query)
        st.markdown(response)
