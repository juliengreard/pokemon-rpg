# --- Base image ---
FROM python:3.10-slim AS base

WORKDIR /app

# Copy production requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source code and data
COPY app ./app
COPY data ./data

# --- Optional dev/test dependencies ---
# ARG to control whether to install test dependencies
ARG INSTALL_DEV=false

# Conditionally install dev/test dependencies
COPY requirements-dev.txt .
RUN if [ "$INSTALL_DEV" = "true" ]; then \
        pip install --no-cache-dir -r requirements-dev.txt; \
    fi

# Always copy tests (so pytest can find them)
COPY tests ./tests

ENV PYTHONPATH=/app

# --- Default CMD for production ---
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
