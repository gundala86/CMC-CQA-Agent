
import re

class IntentExtractionAgent:
    def __init__(self, modalities, phases):
        self.modalities = modalities
        self.phases = phases

        # ✅ Alias mapping for better natural language understanding
        self.modality_aliases = {
            "aav": "AAV Gene Therapy",
            "aav gene therapy": "AAV Gene Therapy",
            "car-t": "CAR-T",
            "cart": "CAR-T",
            "fusion": "Fusion Protein",
            "fusion protein": "Fusion Protein",
            "adc": "ADC",
            "monoclonal antibody": "mAb",
            "mab": "mAb",
            "mrna": "mRNA"
        }

    def extract(self, query):
        query_lower = query.lower()

        # First apply alias mapping
        selected_modality = None
        for alias, canonical in self.modality_aliases.items():
            if alias in query_lower:
                selected_modality = canonical
                break

        # If alias mapping didn't find, fallback to pure string match
        if not selected_modality:
            for modality in self.modalities:
                if modality.lower() in query_lower:
                    selected_modality = modality
                    break

        # Extract phase as before
        selected_phase = None
        for phase in self.phases:
            if phase.lower() in query_lower or phase.replace(" ", "").lower() in query_lower:
                selected_phase = phase
                break

        if not selected_phase:
            phase_match = re.search(r'phase\s*(\d)', query_lower)
            if phase_match:
                phase_num = phase_match.group(1)
                for phase in self.phases:
                    if phase.endswith(phase_num):
                        selected_phase = phase
                        break

        return selected_modality, selected_phase
