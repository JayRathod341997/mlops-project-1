# Use a lightweight official Python image
FROM python:3.11-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies (LightGBM, build essentials)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 build-essential gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Upgrade pip and install dependencies in editable mode
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -e .

# Optional: Train model at build time (only if model is lightweight and always retrained)
RUN python pipeline/training_pipeline.py

# Expose Flask port
EXPOSE 5000

# Run Flask app
CMD ["python", "application.py"]