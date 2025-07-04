FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Verify build context
RUN echo "Build context contents:" && ls -la

# Copy requirements files
COPY setup.py requirements.txt ./

# Verify copied files
RUN echo "Copied files:" && ls -la

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -e .

# Copy remaining files
COPY . .

EXPOSE 5000
CMD ["python", "application.py"]