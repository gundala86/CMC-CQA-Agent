
from agent.knowledge_base_loader import KnowledgeBase
from agent.embedding_model_loader import EmbeddingModel
import pandas as pd
import torch

class SemanticSearchEngine:
    def __init__(self, kb_path):
        self.kb = KnowledgeBase(kb_path)
        self.embedding_model = EmbeddingModel()
        self.df = self.kb.df
        self.embeddings = self.embedding_model.embed(self._generate_context())

    def _generate_context(self):
        self.df['context'] = self.df.apply(
            lambda row: f"Modality: {row['Modality']}, Phase: {row['Phase']}, CQA: {row['CQA']}, Test: {row['Test Methods']}, Control: {row['Control Action']}",
            axis=1
        )
        return self.df['context'].tolist()

    def query(self, user_query, top_k=10):
        query_embedding = self.embedding_model.embed([user_query])
        cosine_scores = torch.nn.functional.cosine_similarity(query_embedding, self.embeddings)
        top_results = torch.topk(cosine_scores, k=top_k)

        results = []
        for score, idx in zip(top_results.values, top_results.indices):
            row = self.df.iloc[idx.item()]
            results.append({
                "Modality": row['Modality'],
                "Phase": row['Phase'],
                "CQA": row['CQA'],
                "Test Methods": row['Test Methods'],
                "Control Action": row['Control Action'],
                "Score": float(score)
            })

        return pd.DataFrame(results)
