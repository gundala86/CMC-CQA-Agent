
import pdfplumber
import pandas as pd
import re
import os

class IngestionEngine:
    def __init__(self, knowledgebase_path):
        self.kb_path = knowledgebase_path
        self.df = pd.read_csv(knowledgebase_path)
        self.df.fillna("", inplace=True)

    def extract_text_from_pdf(self, pdf_path):
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text

    def simple_rule_based_extraction(self, text):
        # Simplified rule-based extraction logic (expandable later with LLMs)
        cqa_matches = []
        lines = text.split("\n")
        for line in lines:
            if "purity" in line.lower() or "potency" in line.lower() or "identity" in line.lower():
                cqa_matches.append(line.strip())
        return cqa_matches

    def expand_knowledgebase(self, extracted_lines, modality, phase):
        new_records = []
        for line in extracted_lines:
            if "purity" in line.lower():
                new_records.append({
                    "Modality": modality, "Phase": phase, "CQA": "Purity",
                    "Test Methods": "HPLC", "Justification": "Extracted from ingestion",
                    "Regulatory Source": "PDF", "Control Action": "Specification"
                })
            if "potency" in line.lower():
                new_records.append({
                    "Modality": modality, "Phase": phase, "CQA": "Potency",
                    "Test Methods": "Bioassay", "Justification": "Extracted from ingestion",
                    "Regulatory Source": "PDF", "Control Action": "Specification"
                })
            if "identity" in line.lower():
                new_records.append({
                    "Modality": modality, "Phase": phase, "CQA": "Identity",
                    "Test Methods": "Peptide Mapping", "Justification": "Extracted from ingestion",
                    "Regulatory Source": "PDF", "Control Action": "Specification"
                })

        if new_records:
            new_df = pd.DataFrame(new_records)
            self.df = pd.concat([self.df, new_df], ignore_index=True)
            self.df.to_csv(self.kb_path, index=False)
            return len(new_records)
        else:
            return 0

    def ingest_pdf(self, pdf_path, modality, phase):
        text = self.extract_text_from_pdf(pdf_path)
        extracted_cqas = self.simple_rule_based_extraction(text)
        added = self.expand_knowledgebase(extracted_cqas, modality, phase)
        return added
