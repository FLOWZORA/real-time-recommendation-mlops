import sys
import subprocess
from pathlib import Path
import mlflow
from mlflow_config import *

repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

def trigger_retraining(wait=False):
    print("[INFO] Drift detected -> triggering retraining")

    try:
        with mlflow.start_run(run_name="drift_retraining"):
            mlflow.log_param("trigger", "drift")
    except Exception as e:
        print(f"[WARN] MLflow run logging skipped ({e})")

    train_script = repo_root / "retrieval" / "train.py"
    proc = subprocess.Popen(
        [sys.executable, str(train_script)],
        cwd=str(repo_root),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    if wait:
        proc.wait()
        print(f"[OK] Triggered retraining completed with code {proc.returncode}")

    return proc

if __name__ == "__main__":
    trigger_retraining(wait=True)

