FROM python:3.10-slim

WORKDIR /app

# Install basic build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip setuptools wheel

COPY requirements.txt .

# Install dependencies using CPU PyTorch wheel index
RUN pip install --no-cache-dir -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu

COPY . .

# Intercept uvicorn so even if Railway UI executes 'uvicorn ... --port $PORT', it never crashes
RUN cp run_server.py /usr/local/bin/uvicorn && chmod +x /usr/local/bin/uvicorn

ENV PYTHONUNBUFFERED=1

EXPOSE 8080
EXPOSE 8000

CMD ["python", "run_server.py", "serving.app:app", "--host", "0.0.0.0", "--port", "8080"]
