
import streamlit as st
from agent.ingestion_engine_ai import IngestionEngineAI
import os

st.set_page_config(page_title="CMC Agent Phase 8: AI Ingestion", page_icon="🤖", layout="wide")
st.title("🤖 CMC AI Knowledge Ingestion Engine (Phase 8 MVP)")

kb_path = "output/CQA_KnowledgeBase_Master.csv"
engine = IngestionEngineAI(kb_path)

uploaded_file = st.file_uploader("Upload regulatory PDF for AI extraction", type=["pdf"])
modality = st.text_input("Specify Modality for extracted CQAs (ex: mAb, ADC, CAR-T, AAV Gene Therapy):")
phase = st.text_input("Specify Phase (ex: Phase 1, Phase 2, Phase 3):")

if st.button("Ingest PDF with AI"):
    if not uploaded_file or not modality or not phase:
        st.warning("Please upload a file and specify modality and phase.")
    else:
        with open("uploaded.pdf", "wb") as f:
            f.write(uploaded_file.read())
        count = engine.ingest_pdf("uploaded.pdf", modality, phase)
        st.success(f"AI Ingestion complete. {count} new records added to Knowledge Base.")
