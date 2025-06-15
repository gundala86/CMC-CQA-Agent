
from knowledge_base_loader import KnowledgeBase

class QueryEngine:
    def __init__(self, kb_path):
        self.kb = KnowledgeBase(kb_path)

    def answer_query(self, query):
        query = query.lower()
        modalities = self.kb.get_modalities()
        phases = self.kb.get_phases()

        selected_modality = None
        selected_phase = None

        for m in modalities:
            if m.lower() in query:
                selected_modality = m
                break

        for p in phases:
            if p.lower() in query:
                selected_phase = p
                break

        cqa_terms = ["identity", "purity", "potency", "glycosylation", "charge variants",
                     "deamidation", "oxidation", "fragmentation", "dar", "free drug",
                     "host cell protein", "host cell dna", "linker", "residual", "viability",
                     "transduction", "replication", "cytokine", "mycoplasma", "dsrna", "capping"]

        matched_cqa = None
        for term in cqa_terms:
            if term in query:
                matched_cqa = term
                break

        results = self.kb.query(modality=selected_modality, phase=selected_phase, cqa=matched_cqa)
        if results.empty:
            return "No matching records found for your query."
        
        return results.to_string(index=False)
