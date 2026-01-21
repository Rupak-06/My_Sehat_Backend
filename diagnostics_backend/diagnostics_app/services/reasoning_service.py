from typing import Dict, Any, List
from diagnostics_backend.diagnostics_app.models.schemas import TriageOutputSchema, Question

# --- QUESTION TEMPLATES ---
SYSTEMIC_QUESTIONS = [
    Question(
        id="q_systemic_1",
        text="How high is your fever and how long has it lasted?",
        options=["Low grade (<38C), <2 days", "High grade (>38C), <2 days", "Any fever > 3 days"],
        allow_custom=True
    ),
    Question(
        id="q_systemic_2",
        text="Are you experiencing severe dehydration (dry mouth, no urine)?",
        options=["Yes", "No"],
        allow_custom=False
    )
]

GI_QUESTIONS = [
    Question(
        id="q_gi_1",
        text="Do you have any nausea, vomiting, or diarrhea?",
        options=["Yes, nausea only", "Vomiting", "Diarrhea", "None"],
        allow_custom=True
    )
]

HEADACHE_QUESTIONS = [
    Question(
        id="q_headache_1",
        text="Is the headache throbbing, squeezing, or sharp?",
        options=["Throbbing", "Squeezing (band-like)", "Sharp/Stabbing"],
        allow_custom=True
    )
]

GENERAL_QUESTIONS = [
    Question(
        id="q_general_1",
        text="Can you describe your symptoms in more detail?",
        options=["pain", "weakness", "discomfort"],
        allow_custom=True
    )
]

WOUND_QUESTIONS = [
    Question(
        id="q_wound_1",
        text="Is the wound deep or showing signs of infection (pus, warmth)?",
        options=["Superficial, clean", "Deep, bleeding controlled", "Signs of infection"],
        allow_custom=True
    ),
    Question(
        id="q_wound_2",
        text="Is the bleeding uncontrollable?",
        options=["Yes", "No - stopped with pressure"],
        allow_custom=False
    )
]

SKIN_QUESTIONS = [
    Question(
        id="q_skin_1",
        text="Is the rash itchy or painful?",
        options=["Itchy", "Painful", "Both", "Neither"],
        allow_custom=True
    ),
    Question(
        id="q_skin_2",
        text="Is the rash spreading rapidly?",
        options=["Yes", "No", "Stable"],
        allow_custom=False
    )

]

CONFIRMATION_QUESTION = Question(
    id="q_continue_1",
    text="Do you want to continue (upload another image or describe symptoms) to improve accuracy?",
    options=["Yes, upload another image", "Yes, add symptoms in text", "No, finalize now"],
    allow_custom=False
)

class ReasoningService:
    def __init__(self):
        pass

    async def generate_question(self, session_data: Dict[str, Any]) -> Question:
        """
        Returns a question based on STRICT domain separation and SYMPTOM CATEGORIZATION.
        Rules:
        - input_mode="text" -> Route to specific systemic category (Headache, GI, Fever, General)
        - input_mode="image" -> WOUND vs SKIN based on observations
        """
        input_mode = session_data.get("input_mode", "mixed")
        observations = session_data.get("observations", {}).get("observations", [])
        
        # Context Variables
        severity = session_data.get("severity", "").lower() if session_data.get("severity") else ""
        duration = session_data.get("duration", "").lower() if session_data.get("duration") else ""
        symptoms = session_data.get("symptoms", "").lower()

        # FIX 3: TEXT TRIAGE SAFETY RULE
        if input_mode == "text":
            # 1. PARSE & CATEGORIZE
            # Categories: infection_risk, headache, mild_gi, vomiting, general
            
            # Keywords
            infection_kws = ["fever", "chills", "shivering", "hot"]
            headache_kws = ["headache", "head pain", "migraine"]
            gi_kws = ["uneasy", "stomach", "nausea", "indigestion", "bloating", "gas"]
            vomit_kws = ["vomit", "throwing up", "puke"]
            
            has_infection = any(k in symptoms for k in infection_kws)
            has_headache = any(k in symptoms for k in headache_kws)
            has_gi = any(k in symptoms for k in gi_kws)
            has_vomit = any(k in symptoms for k in vomit_kws)
            
            # Duration logic for vomiting (>= 2 days -> Fever/Systemic check)
            # Stub: check for "2 days", "3 days", "week"
            is_long_duration = any(t in duration for t in ["2 day", "3 day", "4 day", "5 day", "week"])
            
            # 2. SELECT QUESTION
            
            # Priority A: Infection/Fever keywords -> FORCE FEVER Q
            if has_infection:
                return SYSTEMIC_QUESTIONS[0]
            
            # Priority B: Vomiting + Long Duration -> FEVER Q (Risk of systemic issue)
            if has_vomit and is_long_duration:
                return SYSTEMIC_QUESTIONS[0]
                
            # Priority C: Headache -> HEADACHE Q
            if has_headache:
                return HEADACHE_QUESTIONS[0]
            
            # Priority D: Mild GI / Vomiting (short term) -> GI Q
            if has_gi or has_vomit:
                return GI_QUESTIONS[0]
                
            # Priority E: General -> GENERAL Q (Default)
            # Fever question must NOT be default
            return GENERAL_QUESTIONS[0]

        if input_mode == "image" or input_mode == "mixed":
            if "open wound" in observations or "bleeding" in observations:
                return WOUND_QUESTIONS[0]
            elif "redness" in observations or "rash" in observations:
                return SKIN_QUESTIONS[0]
            
            # If mixed (image + text) and no specific image observations, check text symptoms
            if input_mode == "mixed" and symptoms:
                 # Re-use text logic for mixed fallback
                 infection_kws = ["fever", "chills", "shivering", "hot"]
                 headache_kws = ["headache", "head pain", "migraine"]
                 gi_kws = ["uneasy", "stomach", "nausea", "indigestion", "bloating", "gas"]
                 vomit_kws = ["vomit", "throwing up", "puke"]
                 
                 if any(k in symptoms for k in infection_kws): return SYSTEMIC_QUESTIONS[0]
                 if any(k in symptoms for k in headache_kws): return HEADACHE_QUESTIONS[0]
                 if any(k in symptoms for k in gi_kws) or any(k in symptoms for k in vomit_kws): return GI_QUESTIONS[0]
        
        # Default Fallback (should be Systemic if unknown)
        return SYSTEMIC_QUESTIONS[0]

    async def analyze_symptoms(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Returns a final triage result based on STRICT DOMAIN.
        """
        input_mode = session_data.get("input_mode", "mixed")
        observations = session_data.get("observations", {}).get("observations", [])
        
        # 1. TEXT ONLY -> SYSTEMIC (Simple Stub logic enforced)
        if input_mode == "text":
             return self._get_systemic_response()

        # 2. IMAGE/MIXED -> Check Observations
        if "open wound" in observations or "bleeding" in observations:
            return self._get_wound_response()
        
        elif "redness" in observations or "rash" in observations:
            return self._get_skin_response()

        # Default
        return self._get_systemic_response()
    
    # --- Response Helpers ---
    def _get_systemic_response(self):
        return {
            "summary": "Symptoms consistent with a viral illness or systemic infection.",
            "severity": "medium",
            "possible_causes": [
                { "name": "Viral Influenza", "confidence": 0.78 },
                { "name": "Common Cold", "confidence": 0.65 }
            ],
            "home_care": ["Rest and hydration", "Over-the-counter antipyretics"],
            "prevention": ["Wash hands frequently"],
            "red_flags": ["Stiff neck", "Confusion", "Difficulty breathing"],
            "when_to_seek_care": ["If fever persists > 3 days", "If unable to keep fluids down"],
            "disclaimer": "This is not a medical diagnosis. Consult a professional."
        }

    def _get_wound_response(self):
        return {
            "summary": "Observation of an open wound.",
            "severity": "medium",
            "possible_causes": [
                { "name": "Laceration", "confidence": 0.85 },
                { "name": "Abrasion", "confidence": 0.80 }
            ],
            "home_care": ["Clean with water", "Apply antibiotic ointment", "Cover with sterile bandage"],
            "prevention": ["Keep environment safe"],
            "red_flags": ["Uncontrollable bleeding", "Signs of infection (pus, red streaks)"],
            "when_to_seek_care": ["If wound is deep (needs stitches)", "If bleeding doesn't stop"],
            "disclaimer": "This is not a medical diagnosis. Consult a professional."
        }

    def _get_skin_response(self):
        return {
            "summary": "Symptoms suggest a localized skin reaction.",
            "severity": "low",
            "possible_causes": [
                { "name": "Contact Dermatitis", "confidence": 0.75 },
                { "name": "Insect Bite", "confidence": 0.60 }
            ],
            "home_care": ["Keep clean and dry", "Apply cold compress"],
            "prevention": ["Avoid potential allergens"],
            "red_flags": ["Rapidly spreading redness", "High fever"],
            "when_to_seek_care": ["If symptoms worsen after 24 hours"],
            "disclaimer": "This is not a medical diagnosis. Consult a professional."
        }
