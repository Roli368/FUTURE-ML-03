# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download Spacy  model
RUN python -m spacy download en_core_web_sm

# Copy project
COPY . .

# Train the Skill Extractor (Generate Artifacts)
RUN python trainer.py

# Create uploads directory (if not handled by trainer.py or for runtime safety)
RUN mkdir -p uploads

# Expose port
EXPOSE 5000

# Command to run the application using Gunicorn with dynamic port
CMD sh -c "gunicorn --bind 0.0.0.0:${PORT:-5000} app:app"
