# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VENV_PATH=/opt/venv

# Install system dependencies (LightGBM + build essentials)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python -m venv $VENV_PATH
ENV PATH="$VENV_PATH/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
# COPY pyproject.toml .
# COPY setup.cfg .
# COPY setup.py .

# Install project in editable mode with pip
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -e .

# Copy remaining project files
COPY . .

# Expose port (optional - better to specify in run command)
EXPOSE 5000

# Run application (consider using gunicorn for production)
CMD ["python", "application.py"]