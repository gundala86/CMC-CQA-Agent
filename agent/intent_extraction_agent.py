
import re

class IntentExtractionAgent:
    def __init__(self, modalities, phases):
        self.modalities = modalities
        self.phases = phases

    def extract(self, query):
        query_lower = query.lower()

        selected_modality = None
        selected_phase = None

        for modality in self.modalities:
            if modality.lower() in query_lower:
                selected_modality = modality
                break

        for phase in self.phases:
            if phase.lower() in query_lower or phase.replace(" ", "").lower() in query_lower:
                selected_phase = phase
                break

        # Additional simple fallback using regex for "phase X"
        if not selected_phase:
            phase_match = re.search(r'phase\s*(\d)', query_lower)
            if phase_match:
                phase_num = phase_match.group(1)
                for phase in self.phases:
                    if phase.endswith(phase_num):
                        selected_phase = phase
                        break

        return selected_modality, selected_phase
