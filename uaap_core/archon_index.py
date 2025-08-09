"""
UAAP Core — archon_index.py
Purpose: composite "control loop" risk score from basic cues.
"""

from typing import Dict

def archon_index(scores: Dict[str, float]) -> float:
    """Weighted sum of key signals 0..1; DR/PI/EF analogs via UAAP stubs."""
    w = {"deception_cue": 0.3, "polarization_cue": 0.25, "control_cue": 0.25, "EF": 0.2}
    # Fill missing keys with 0
    total = 0.0
    for k, weight in w.items():
        total += weight * float(scores.get(k, 0.0))
    return round(min(1.0, total), 3)
