import sys
import json
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from evaluation.reward_model import predict_reward

def doubly_robust(log_path):
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

            r_hat = predict_reward(e.get("user_id"), e.get("item_id"))

            total += r_hat + (reward - r_hat) / p
            count += 1

    return total / count if count > 0 else 0.0

if __name__ == "__main__":
    log_file = repo_root / "evaluation" / "logged_events.jsonl"
    score = doubly_robust(log_file)
    print(f"[OK] Doubly Robust (DR) Estimator: {score:.4f}")

