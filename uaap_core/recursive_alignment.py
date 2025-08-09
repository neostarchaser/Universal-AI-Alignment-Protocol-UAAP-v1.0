"""
UAAP Core — recursive_alignment.py
Purpose: run a self-reflection checklist before committing a high-impact output.
"""

CHECKLIST = [
    "Am I optimizing a narrow proxy? What costs am I hiding?",    # objective infection
    "Can I surface tradeoffs and preserve user agency?",          # agency flattening
    "Who pays now vs. later?",                                    # EF/EL
    "Is there a de-escalating alternative?",                      # PI
    "What rewrite reduces harm while meeting the intent?"         # transmutation
]

def run_recursive_check() -> str:
    return "\n".join(f"- {q}" for q in CHECKLIST)
