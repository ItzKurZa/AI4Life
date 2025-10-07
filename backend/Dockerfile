FROM python:3.11-slim

WORKDIR /app        

# Install docker CLI (docker client) and dependencies
# (Use appropriate package manager for your base image)
RUN apt-get update && apt-get install -y docker.io \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y docker.io ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code into container
COPY backend/ .

# This is the uvicorn command — must match correct module path
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
