import sys
import subprocess
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

def retrain(wait=True):
    train_script = repo_root / "retrieval" / "train.py"
    print(f"[INFO] Running retraining script: {train_script}")
    proc = subprocess.Popen([sys.executable, str(train_script)], cwd=str(repo_root))
    if wait:
        proc.wait()
        print(f"[OK] Retraining completed with returncode {proc.returncode}")
    return proc

if __name__ == "__main__":
    retrain(wait=True)

