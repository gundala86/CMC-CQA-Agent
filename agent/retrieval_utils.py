
from agent.semantic_search_engine import SemanticSearchEngine
from agent.knowledge_base_loader import KnowledgeBase

class HybridRetriever:
    def __init__(self, kb_path):
        self.kb_path = kb_path
        self.semantic_engine = SemanticSearchEngine(kb_path)
        self.kb = KnowledgeBase(kb_path)

    def answer(self, user_query):
        semantic_results = self.semantic_engine.query(user_query, top_k=10)
        if semantic_results.empty:
            return "No results found."
        return semantic_results[['Modality', 'Phase', 'CQA', 'Test Methods', 'Control Action']].to_string(index=False)
