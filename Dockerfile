FROM python:3.10-slim

WORKDIR /app

# Install basic build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install CPU-only torch first (180MB vs 2.5GB CUDA) to prevent Railway memory limits
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

EXPOSE 8080
EXPOSE 8000

CMD ["sh", "-c", "python -m uvicorn serving.app:app --host 0.0.0.0 --port ${PORT:-8080}"]
