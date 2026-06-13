# Multi-stage build for Quantum Search in Graph Nodes
FROM python:3.12-slim as base

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM base

# Copy project files
COPY . .

# Expose port for Streamlit
EXPOSE 8501

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Default command runs Streamlit dashboard
CMD ["streamlit", "run", "dashboard/app.py", "--server.port=8501", "--server.address=0.0.0.0"]

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8501')" || exit 1
