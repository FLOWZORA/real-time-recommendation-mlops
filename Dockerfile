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

ENV PYTHONUNBUFFERED=1

EXPOSE 8080
EXPOSE 8000

CMD ["python", "-m", "serving.app"]
