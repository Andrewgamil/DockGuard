FROM python:3.11-slim

# Prevent Python buffering and .pyc creation
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first (caching layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root user for security
RUN adduser --disabled-password --gecos "" appuser && \
    mkdir -p /app/data && \
    chown -R appuser:appuser /app

USER appuser

# Copy the application
COPY --chown=appuser:appuser . .

# Expose the port
EXPOSE 8080

# Run with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]


