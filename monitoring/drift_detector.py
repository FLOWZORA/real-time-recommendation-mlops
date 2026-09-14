import sys
from pathlib import Path
import numpy as np

repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from monitoring.drift_stats import feature_mean, reward_mean

# Baselines (set after training)
BASELINE_FEATURE_MEAN = None
BASELINE_REWARD_MEAN = None

FEATURE_DRIFT_THRESHOLD = 0.3
REWARD_DRIFT_THRESHOLD = 0.2

def set_baseline(features, reward):
    global BASELINE_FEATURE_MEAN, BASELINE_REWARD_MEAN
    BASELINE_FEATURE_MEAN = np.asarray(features, dtype=np.float32)
    BASELINE_REWARD_MEAN = float(reward)
    print(f"[OK] Drift baselines configured: reward={BASELINE_REWARD_MEAN:.4f}")

def detect_drift():
    if BASELINE_FEATURE_MEAN is None or BASELINE_REWARD_MEAN is None:
        return False

    current_feat = feature_mean()
    current_reward = reward_mean()

    if current_feat is None or current_reward is None:
        return False

    feature_shift = np.linalg.norm(current_feat - BASELINE_FEATURE_MEAN)
    reward_shift = abs(current_reward - BASELINE_REWARD_MEAN)

    if feature_shift > FEATURE_DRIFT_THRESHOLD:
        print(f"[WARN] Data drift detected (shift: {feature_shift:.4f} > {FEATURE_DRIFT_THRESHOLD})")
        return True

    if reward_shift > REWARD_DRIFT_THRESHOLD:
        print(f"[WARN] Concept drift detected (shift: {reward_shift:.4f} > {REWARD_DRIFT_THRESHOLD})")
        return True

    return False

if __name__ == "__main__":
    from monitoring.drift_stats import log_feature, log_reward
    set_baseline(np.zeros(8), 1.0)
    for _ in range(10):
        log_feature(np.zeros(8))
        log_reward(1.0)
    print(f"[OK] Drift check with baseline: {detect_drift()}")

