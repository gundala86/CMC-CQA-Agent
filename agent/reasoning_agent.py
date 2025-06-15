
import pandas as pd
from agent.knowledge_base_loader import KnowledgeBase

class ReasoningAgent:
    def __init__(self, kb_path):
        self.kb = KnowledgeBase(kb_path)
        self.df = self.kb.df

    def extract_context(self, user_query):
        modalities = self.kb.get_modalities()
        phases = self.kb.get_phases()
        selected_modality = None
        selected_phase = None

        for m in modalities:
            if m.lower() in user_query.lower():
                selected_modality = m
                break

        for p in phases:
            if p.lower() in user_query.lower():
                selected_phase = p
                break

        return selected_modality, selected_phase

    def generate_control_strategy(self, user_query):
        modality, phase = self.extract_context(user_query)

        if not modality or not phase:
            return "Please specify both modality and phase (ex: 'Fusion Protein Phase 3')."

        df_filtered = self.df[
            (self.df['Modality'].str.lower() == modality.lower()) &
            (self.df['Phase'].str.lower() == phase.lower())
        ]

        if df_filtered.empty:
            return f"No control strategy data found for {modality} in {phase}."

        grouped = df_filtered.groupby("CQA")
        output = []

        for cqa, group in grouped:
            tests = ", ".join(group["Test Methods"].unique())
            control_action = ", ".join(group["Control Action"].unique())
            justifications = ", ".join(group["Justification"].unique())
            output.append(f"**CQA:** {cqa}\n- Test Methods: {tests}\n- Control Action: {control_action}\n- Justification: {justifications}\n")

        strategy = "\n\n".join(output)
        return f"### Control Strategy for {modality} ({phase}):\n\n{strategy}"
