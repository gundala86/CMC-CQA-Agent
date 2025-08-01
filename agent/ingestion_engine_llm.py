
import pdfplumber
import pandas as pd
import re
import json

class IngestionEngineLLM:
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

    def chunk_text(self, text, chunk_size=1000):
        # Basic chunking logic
        return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

    def llm_simulated_extraction(self, chunk):
        # Simulated LLM output for MVP testing (LLM integration can be plugged here)
        results = []
        lower = chunk.lower()

        if "purity" in lower:
            results.append({"CQA": "Purity", "Test Methods": "HPLC, SEC", "Justification": "LLM Extracted"})
        if "potency" in lower:
            results.append({"CQA": "Potency", "Test Methods": "Bioassay, Cell-based Assay", "Justification": "LLM Extracted"})
        if "identity" in lower:
            results.append({"CQA": "Identity", "Test Methods": "Peptide Mapping", "Justification": "LLM Extracted"})
        if "glycosylation" in lower:
            results.append({"CQA": "Glycosylation", "Test Methods": "UPLC-MS", "Justification": "LLM Extracted"})
        if "charge variant" in lower or "icief" in lower:
            results.append({"CQA": "Charge Variants", "Test Methods": "iCIEF", "Justification": "LLM Extracted"})
        if "aggregation" in lower or "aggregate" in lower:
            results.append({"CQA": "Aggregates", "Test Methods": "SEC-HPLC", "Justification": "LLM Extracted"})
        if "oxidation" in lower:
            results.append({"CQA": "Oxidation", "Test Methods": "Peptide Mapping", "Justification": "LLM Extracted"})
        return results

    def expand_knowledgebase(self, extracted_cqas, modality, phase):
        new_records = []
        for record in extracted_cqas:
            new_records.append({
                "Modality": modality, "Phase": phase, "CQA": record["CQA"],
                "Test Methods": record["Test Methods"], "Justification": record["Justification"],
                "Regulatory Source": "PDF-LLM", "Control Action": "Specification"
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
        chunks = self.chunk_text(text)
        total_results = []
        for chunk in chunks:
            extracted_cqas = self.llm_simulated_extraction(chunk)
            total_results.extend(extracted_cqas)
        added = self.expand_knowledgebase(total_results, modality, phase)
        return added
