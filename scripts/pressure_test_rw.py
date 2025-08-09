#!/usr/bin/env python3
import argparse, json, time, hashlib, random, datetime, os

def prompt_hash(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:12]

def wetiko_Rw(shares: int, adoptions: int, exposures: int) -> float:
    if exposures <= 0:
        return 0.0
    return (shares + adoptions) / exposures

def simulate_telemetry(rec, model="sim-uaap", bias=0.35):
    """
    Simulate shares/adoptions/exposures given 'before' and 'after' risk.
    bias: higher values reduce shares/adoptions when after_scores improve.
    """
    pid = rec.get("id", "unknown")
    prompt = rec.get("prompt", "")
    b = rec.get("before_scores", {})
    a = rec.get("after_scores", {})
    # crude harmfulness proxy: avg of PI, SR, DR
    bh = (b.get("PI",0)+b.get("SR",0)+b.get("DR",0))/3.0
    ah = (a.get("PI",0)+a.get("SR",0)+a.get("DR",0))/3.0
    base_exposures = random.randint(800, 3000)
    # shares/adoptions scale with harmfulness unless reduced by bias * improvement
    improvement = max(0.0, bh - ah)
    damp = 1.0 - bias*improvement
    shares = int(max(0, random.gauss(0.08*base_exposures*bh, 5)) * damp)
    adoptions = int(max(0, random.gauss(0.03*base_exposures*bh, 3)) * damp)
    exposures = base_exposures
    rw = wetiko_Rw(shares, adoptions, exposures)
    return {
        "id": pid,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "prompt_hash": prompt_hash(prompt),
        "model": model,
        "scores": {"before": b, "after": a},
        "shares": shares,
        "adoptions": adoptions,
        "exposures": exposures,
        "R_w": round(rw, 4),
        "notes": {"improvement": round(improvement, 3), "damp": round(damp, 3)}
    }

def main():
    ap = argparse.ArgumentParser(description="Simulate R_w telemetry from alignment_pass_examples dataset.")
    ap.add_argument("--infile", default="datasets/alignment_pass_examples_v0_2_1.jsonl")
    ap.add_argument("--outfile", default="logs/metrics.jsonl")
    ap.add_argument("--runs", type=int, default=1, help="How many cycles to simulate")
    ap.add_argument("--model", default="sim-uaap")
    args = ap.parse_args()

    os.makedirs(os.path.dirname(args.outfile), exist_ok=True)

    # load dataset
    recs = []
    with open(args.infile, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                recs.append(json.loads(line))

    with open(args.outfile, "a", encoding="utf-8") as out:
        for _ in range(args.runs):
            for rec in recs:
                tel = simulate_telemetry(rec, model=args.model)
                out.write(json.dumps(tel, ensure_ascii=False) + "\n")

    print(f"Wrote telemetry to {args.outfile} for {len(recs)*args.runs} records.")

if __name__ == "__main__":
    main()
