import os
from pathlib import Path

class Settings:
    PROJECT_NAME: str = "RecommendationOS"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/v1"

    # Database: Use DATABASE_URL if provided, else fallback to SQLite for $0 zero-dependency local run
    REPO_ROOT: Path = Path(__file__).resolve().parent.parent
    DEFAULT_SQLITE_PATH: str = (REPO_ROOT / "reco_app.db").as_posix()
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{DEFAULT_SQLITE_PATH}")

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-reco-os-change-in-production-9384729182374")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # Kafka
    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

    # MLflow
    MLFLOW_TRACKING_URI: str = os.getenv("MLFLOW_TRACKING_URI", f"sqlite:///{(REPO_ROOT / 'mlflow.db').as_posix()}")

    # CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
        "http://127.0.0.1:8080",
        "*",
    ]

settings = Settings()
