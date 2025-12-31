# Base Image: Lightweight Python 3.11
FROM python:3.11-slim

# Set environment variables
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to disc
# PYTHONUNBUFFERED: Ensures logs are flushed immediately (vital for Docker logs)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy requirements first to leverage Docker layer caching
# If requirements.txt hasn't changed, this step is cached
COPY requirements.txt .

# Install dependencies
# --no-cache-dir reduces image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Security: Create a non-root user and switch to it
# This prevents the container from running with root privileges on the host
RUN useradd -m appuser && \
    chown -R appuser:appuser /app

USER appuser

# Expose port 8000 for the FastAPI server
EXPOSE 8000

# Command to run the application
# Host 0.0.0.0 makes the server accessible outside the container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]