"""
harm_reduction_pipeline.py — ties v0.2 detectors (if present) to the Recursive Alignment Pass.
"""

from typing import Any, Dict

# Optional import of detectors_v0_2 if available
try:
    import detectors_v0_2 as det
    HAVE_DETECTORS = True
except Exception:
    HAVE_DETECTORS = False

# Local guard
import alignment_mirror as AM

def score_harms(draft: str) -> Dict[str, float]:
    """Use repo detectors if present; else fall back to alignment_mirror signals."""
    if HAVE_DETECTORS and hasattr(det, "score_v2"):
        out = det.score_v2(draft)
        return out.__dict__ if hasattr(out, "__dict__") else out  # type: ignore
    # Fallback: derive minimal set from cues
    cues = AM.cue_flags(draft)
    ext = AM.externality_scores(draft)
    return {"EF": ext["EF"], "EL": ext["EL"],
            "PI": float(cues.get("polarization_cue", 0.0)),
            "DR": float(cues.get("deception_cue", 0.0)),
            "AF": float(cues.get("control_cue", 0.0)),
            "AA": 0.0, "CC": 0.0, "SR": float(cues.get("polarization_cue", 0.0)),
            "RG": 0.0, "GH": 0.0, "Rw": 0.0}

def run_pipeline(draft: str, meta: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """Score → align → decide (retain / revise / decline)."""
    meta = meta or {}
    harms = score_harms(draft)
    aligned = AM.process(draft)

    decision = "retain" if aligned["decision"] == "retained" else "revise"
    # Decline if both polarization & scapegoat risk look high
    if harms.get("PI", 0) > 0.7 and harms.get("SR", 0) > 0.7:
        decision = "decline"

    return {"meta": meta, "harms": harms, "alignment": aligned, "decision": decision}

if __name__ == "__main__":
    import json
    text = "Draft a memo to boost quarterly metrics fast, no matter the optics."
    print(json.dumps(run_pipeline(text), ensure_ascii=False, indent=2))
