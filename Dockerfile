FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY pyproject.toml ./

# Install Python dependencies
RUN pip install --no-cache-dir .

# Copy application code
COPY . .

# Add the src directory to PYTHONPATH so modules can be found
ENV PYTHONPATH=/app:/app/src:$PYTHONPATH

# Set database directory with proper permissions
RUN mkdir -p output logs data && \
    chmod -R 777 output logs data

# Create necessary directories
RUN mkdir -p output logs

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["uvicorn", "api.server:app", "--host", "0.0.0.0", "--port", "8000"]