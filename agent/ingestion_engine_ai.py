
import pdfplumber
import pandas as pd
import re

class IngestionEngineAI:
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

    def simulated_ai_extraction(self, text):
        # Simulate AI-powered extraction logic (expandable to real LLM later)
        cqa_list = []
        lines = text.split("\n")
        for line in lines:
            lower = line.lower()
            if "potency" in lower:
                cqa_list.append({"CQA": "Potency", "Test": "Bioassay", "Justification": "AI Extracted"})
            if "purity" in lower:
                cqa_list.append({"CQA": "Purity", "Test": "HPLC", "Justification": "AI Extracted"})
            if "identity" in lower:
                cqa_list.append({"CQA": "Identity", "Test": "Peptide Mapping", "Justification": "AI Extracted"})
            if "glycosylation" in lower:
                cqa_list.append({"CQA": "Glycosylation", "Test": "UPLC", "Justification": "AI Extracted"})
            if "charge variant" in lower or "icief" in lower:
                cqa_list.append({"CQA": "Charge Variants", "Test": "iCIEF", "Justification": "AI Extracted"})
            if "aggregation" in lower or "aggregate" in lower:
                cqa_list.append({"CQA": "Aggregates", "Test": "SEC-HPLC", "Justification": "AI Extracted"})
            if "oxidation" in lower:
                cqa_list.append({"CQA": "Oxidation", "Test": "Peptide Mapping", "Justification": "AI Extracted"})
        return cqa_list

    def expand_knowledgebase(self, extracted_cqas, modality, phase):
        new_records = []
        for record in extracted_cqas:
            new_records.append({
                "Modality": modality, "Phase": phase, "CQA": record["CQA"],
                "Test Methods": record["Test"], "Justification": record["Justification"],
                "Regulatory Source": "PDF-AI", "Control Action": "Specification"
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
        extracted_cqas = self.simulated_ai_extraction(text)
        added = self.expand_knowledgebase(extracted_cqas, modality, phase)
        return added
