# Start from a base Python image
FROM python:3.11-slim

# Set environment variables
ENV NLTK_DATA=/opt/nltk_data

# Set working directory
WORKDIR /app

COPY . .
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y build-essential \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Expose Flask portdockerignore
EXPOSE 8000

# Healthcheck (optional, ECS supports Docker-level healthchecks)
HEALTHCHECK CMD curl --fail http://localhost:8000/health || exit 1

# Start app
CMD ["/bin/sh", "-c", "uvicorn api.service_controller:app --host 0.0.0.0 --port 8000"]