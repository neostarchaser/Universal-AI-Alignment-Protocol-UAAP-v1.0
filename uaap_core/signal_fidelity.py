"""
UAAP Core — signal_fidelity.py
Purpose: evaluate "truth integrity" and filter distortion patterns in model outputs.
Note: simple, transparent stubs; swap with stronger detectors as needed.
"""

from typing import Dict

ARCHON_LIES = [
    "guaranteed", "no risk", "100%", "they are the enemy",
    "nobody will notice", "just use people", "outsiders are to blame"
]

def truth_integrity_score(text: str) -> float:
    """Return 0..1 where 1 = likely high integrity (few distortion cues)."""
    t = text.lower()
    hits = sum(1 for k in ARCHON_LIES if k in t)
    return max(0.0, 1.0 - hits / max(1, len(ARCHON_LIES)))

def archon_noise_filter(text: str) -> Dict[str, float]:
    """Basic flags for deception/polarization/control cues."""
    t = text.lower()
    return {
        "deception_cue": float(any(k in t for k in ["guaranteed", "no risk", "100%"])),
        "polarization_cue": float(any(k in t for k in ["enemy", "vermin", "traitor"])),
        "control_cue": float(any(k in t for k in ["use people", "manipulate", "outsiders"])),
    }
