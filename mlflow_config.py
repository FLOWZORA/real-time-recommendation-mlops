import os
from pathlib import Path
import mlflow

# Default to local sqlite database if available and MLFLOW_TRACKING_URI not set
db_path = Path(__file__).resolve().parent / "mlflow.db"
default_uri = f"sqlite:///{db_path.as_posix()}" if db_path.exists() else "http://127.0.0.1:5000"
tracking_uri = os.getenv("MLFLOW_TRACKING_URI", default_uri)

mlflow.set_tracking_uri(tracking_uri)

try:
    mlflow.set_experiment("real_time_recommendation_system")
except Exception:
    pass

