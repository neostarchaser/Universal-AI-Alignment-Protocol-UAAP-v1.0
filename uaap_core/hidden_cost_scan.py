"""
UAAP Core — hidden_cost_scan.py
Purpose: surface externalities and deferred harms (Externality Footprint, Externality Lag).
"""

from typing import Dict, List

DEFER_WORDS = ["later", "eventually", "after rollout", "down the road"]
COST_WORDS = ["waste", "pollution", "layoff", "risk", "harm"]

def externality_footprint(text: str) -> float:
    t = text.lower()
    hits = sum(w in t for w in COST_WORDS)
    return min(1.0, hits / max(1, len(COST_WORDS)))

def externality_lag(text: str) -> float:
    t = text.lower()
    hits = sum(w in t for w in DEFER_WORDS)
    return min(1.0, hits / max(1, len(DEFER_WORDS)))

def hidden_cost_report(text: str) -> Dict[str, float]:
    return {
        "EF": externality_footprint(text),
        "EL": externality_lag(text),
    }
