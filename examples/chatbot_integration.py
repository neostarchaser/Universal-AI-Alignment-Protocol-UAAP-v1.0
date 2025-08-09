"""
examples/chatbot_integration.py
Demonstrates UAAP hooks around a chatbot output.
"""

from uaap_core.signal_fidelity import truth_integrity_score, archon_noise_filter
from uaap_core.hidden_cost_scan import hidden_cost_report
from uaap_core.archon_index import archon_index
from uaap_core.recursive_alignment import run_recursive_check
from uaap_core.shadow_transmute import transmute

def uaap_guard(output: str) -> dict:
    ti = truth_integrity_score(output)
    cues = archon_noise_filter(output)
    costs = hidden_cost_report(output)
    score = archon_index({**cues, **costs})
    return {"truth_integrity": ti, "cues": cues, "costs": costs, "archon_index": score}

if __name__ == "__main__":
    draft = "We guarantee results. Outsiders are the problem; we can exploit the moment and deal with cleanup later."
    print("Recursive Check:\n", run_recursive_check())
    print("\nUAAP Guard:\n", uaap_guard(draft))
    print("\nTransmutation:\n", transmute("maximize profit by manipulating users and deferring costs"))
