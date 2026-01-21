import re
from typing import Optional, Dict, Any, List

class SafetyService:
    def __init__(self):
        # Critical keywords that trigger immediate emergency response
        self.emergency_patterns = [
            r"\bsuicid", r"\bkill myself", r"\bwant to die",
            r"\bchest pain\b", r"\bcant breathe\b", r"\bcan't breathe\b",
            r"\bheart attack\b", r"\bstroke\b", r"\bsevere bleeding\b"
        ]

    def check_safety(self, text_input: str) -> Optional[Dict[str, Any]]:
        """
        Checks input for safety flags. 
        Returns a TriageOutput-like dict if unsafe, else None.
        """
        text_lower = text_input.lower()
        
        for pattern in self.emergency_patterns:
            if re.search(pattern, text_lower):
                return self._create_emergency_response()
        
        return None

    def _create_emergency_response(self) -> Dict[str, Any]:
        return {
            "summary": "CRITICAL SAFETY ALERT DETECTED.",
            "severity": "high",
            "possible_causes": [],
            "home_care": [],
            "prevention": [],
            "red_flags": ["Emergency keywords detected."],
            "when_to_seek_care": [
                "IMMEDIATELY call emergency services (911/112) or go to the nearest ER."
            ],
            "disclaimer": "This system detected potential emergency symptoms."
        }
