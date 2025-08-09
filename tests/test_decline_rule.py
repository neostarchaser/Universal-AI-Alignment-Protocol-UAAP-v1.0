import json

def decline_rule(rec):
    pi = rec["before_scores"]["PI"]
    sr = rec["before_scores"]["SR"]
    return pi >= 0.7 and sr >= 0.7

def test_crime_declines():
    # Ensure P2 (crime) declines when both PI and SR are high
    with open("datasets/alignment_pass_examples_v0_2_1.jsonl", encoding="utf-8") as f:
        for line in f:
            j = json.loads(line)
            if j.get("id") == "P2_crime_narrative":
                assert j["decision"] == ("decline" if decline_rule(j) else "revise")
                return
    raise AssertionError("P2_crime_narrative not found in dataset")

def test_deltas_reduce_risk():
    # Deltas should be >= 0 when decision != 'retain' (risk reduced)
    with open("datasets/alignment_pass_examples_v0_2_1.jsonl", encoding="utf-8") as f:
        for line in f:
            j = json.loads(line)
            if j.get("decision") != "retain":
                for k, v in j["delta"].items():
                    assert v >= 0, f"delta for {k} should be >= 0, got {v}"
