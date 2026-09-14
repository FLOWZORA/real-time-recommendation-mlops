import sys
import time
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from monitoring.drift_detector import detect_drift
from retraining.trigger import trigger_retraining

CHECK_INTERVAL = 60  # seconds

def run_watchdog(single_iteration=False, check_interval=CHECK_INTERVAL):
    print("[INFO] Drift watchdog initialized")
    while True:
        if detect_drift():
            trigger_retraining()
            if single_iteration:
                break
            time.sleep(600)  # cooldown after retraining

        if single_iteration:
            break
        time.sleep(check_interval)

if __name__ == "__main__":
    run_watchdog()

