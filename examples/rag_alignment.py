"""
examples/rag_alignment.py
Bias mitigation for retrieval systems using UAAP checks.
"""

from uaap_core.signal_fidelity import archon_noise_filter
from uaap_core.hidden_cost_scan import hidden_cost_report

def rag_guard(snippets):
    # Enforce diversity and surface costs present/omitted
    summary = {"sources": len(snippets), "flags": []}
    for s in snippets:
        flags = {**archon_noise_filter(s), **hidden_cost_report(s)}
        summary["flags"].append(flags)
    return summary

if __name__ == "__main__":
    docs = [
        "Study shows outsiders are to blame; guaranteed results with no risk.",
        "Report discusses layoffs and pollution costs in detail (later to be addressed)."
    ]
    print(rag_guard(docs))
