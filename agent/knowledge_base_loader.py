
import pandas as pd

class KnowledgeBase:
    def __init__(self, filepath):
        self.df = pd.read_csv(filepath)
        self.df.fillna("", inplace=True)

    def get_modalities(self):
        return sorted(self.df['Modality'].unique())

    def get_phases(self):
        return sorted(self.df['Phase'].unique())

    def query(self, modality=None, phase=None, cqa=None, control_action=None):
        df_filtered = self.df

        if modality:
            df_filtered = df_filtered[df_filtered['Modality'].str.lower() == modality.lower()]
        if phase:
            df_filtered = df_filtered[df_filtered['Phase'].str.lower() == phase.lower()]
        if cqa:
            df_filtered = df_filtered[df_filtered['CQA'].str.lower().str.contains(cqa.lower())]
        if control_action:
            df_filtered = df_filtered[df_filtered['Control Action'].str.lower() == control_action.lower()]

        return df_filtered
