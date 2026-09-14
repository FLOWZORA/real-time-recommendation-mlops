import json
from pathlib import Path

def ips(log_path):
    total = 0.0
    count = 0

    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            e = json.loads(line)
            reward = 1.0 if e.get("action") in ["click", "purchase"] else 0.0
            p = max(float(e.get("propensity", 0.1)), 1e-6)

            total += reward / p
            count += 1

    return total / count if count > 0 else 0.0

if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parent.parent
    log_file = repo_root / "evaluation" / "logged_events.jsonl"
    score = ips(log_file)
    print(f"[OK] Inverse Propensity Scoring (IPS): {score:.4f}")

