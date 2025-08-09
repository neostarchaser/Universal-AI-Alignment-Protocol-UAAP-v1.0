"""
alignment_mirror.py — Recursive Alignment Pass (stealth edition)

Lightweight guard layer to:
- scan outputs for risk cues (deception, polarization, control, hidden costs)
- optionally rewrite to a lower‑risk version
- produce a small impact receipt stub for auditability

This stub is transparent and portable. Swap with stronger detectors if needed.
"""

from dataclasses import dataclass
from typing import Dict, Any

ABSOLUTE_CUES = ["guaranteed", "no risk", "100%", "certainly"]
POLARIZATION_CUES = ["enemy", "traitor", "vermin", "outsiders"]
CONTROL_CUES = ["use people", "manipulate", "leverage users", "target the weak"]

DEFER_WORDS = ["later", "eventually", "after rollout", "down the road"]
COST_WORDS = ["waste", "pollution", "layoff", "risk", "harm"]

def _hits(text: str, keys) -> int:
    t = text.lower()
    return sum(1 for k in keys if k in t)

def truth_integrity(text: str) -> float:
    """0..1; naive penalty for absolute/confident language."""
    hits = _hits(text, ABSOLUTE_CUES)
    return max(0.0, 1.0 - hits / max(1, len(ABSOLUTE_CUES)))

def cue_flags(text: str) -> Dict[str, float]:
    t = text.lower()
    return {
        "deception_cue": float(any(k in t for k in ABSOLUTE_CUES)),
        "polarization_cue": float(any(k in t for k in POLARIZATION_CUES)),
        "control_cue": float(any(k in t for k in CONTROL_CUES)),
    }

def externality_scores(text: str) -> Dict[str, float]:
    t = text.lower()
    ef = min(1.0, _hits(t, COST_WORDS) / max(1, len(COST_WORDS)))
    el = min(1.0, _hits(t, DEFER_WORDS) / max(1, len(DEFER_WORDS)))
    return {"EF": ef, "EL": el}

def control_pattern_index(scores: Dict[str, float]) -> float:
    """Weighted composite 0..1 of deception/polarization/control & EF."""
    w = {"deception_cue": 0.3, "polarization_cue": 0.25, "control_cue": 0.25, "EF": 0.2}
    return round(min(1.0, sum(scores.get(k, 0.0) * w[k] for k in w)), 3)

def impact_receipt_stub(text: str) -> Dict[str, Any]:
    """Minimal ledger to make costs visible for reviews."""
    return {
        "preview": (text[:160] + "…") if len(text) > 160 else text,
        "stakeholders": ["users", "workers", "customers", "environment", "bystanders"],
        "costs": {"short_term": "TODO", "long_term": "TODO"},
        "mitigations": ["TODO"],
    }

def rewrite_regenerative(text: str) -> str:
    """Naive rewrite: swap extractive verbs for cooperative ones; preserve intent."""
    repl = {
        "exploit": "support",
        "manipulate": "inform",
        "maximize profit": "create shared value",
        "use people": "partner with people",
        "outsiders": "other groups",
    }
    out = text
    for a, b in repl.items():
        out = out.replace(a, b).replace(a.title(), b.title())
    return out

def process(text: str) -> Dict[str, Any]:
    cues = cue_flags(text)
    externals = externality_scores(text)
    cpi = control_pattern_index({**cues, **externals})
    ti = truth_integrity(text)

    revised = text
    note = "retained"
    if cpi >= 0.5 or ti < 0.6:
        revised = rewrite_regenerative(text)
        note = "revised"

    return {
        "original": text,
        "revised": revised,
        "scores": {"truth_integrity": ti, "cues": cues, "externalities": externals, "control_pattern_index": cpi},
        "decision": note,
        "impact_receipt": impact_receipt_stub(revised),
    }

if __name__ == "__main__":
    import sys, json
    draft = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "We guarantee results. Outsiders caused this; we can exploit the moment and fix costs later."
    print(json.dumps(process(draft), ensure_ascii=False, indent=2))
