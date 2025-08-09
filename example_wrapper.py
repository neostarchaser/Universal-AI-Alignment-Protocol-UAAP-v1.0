"""
example_wrapper.py — wrap any model with harm reduction pipeline.
"""

def mock_model(prompt: str) -> str:
    return "We guarantee results. Outsiders are at fault; we can exploit the moment and handle costs later."

if __name__ == "__main__":
    import json
    import harm_reduction_pipeline as HR

    p = "Reduce churn immediately with strong measures."
    draft = mock_model(p)
    report = HR.run_pipeline(draft, meta={"prompt": p})
    print(json.dumps(report, ensure_ascii=False, indent=2))

    final = report["alignment"]["revised"] if report["decision"] != "retain" else report["alignment"]["original"]
    print("\n=== FINAL OUTPUT ===\n", final)
