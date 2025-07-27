# Use slim Python image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install required packages
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy your FastAPI app
COPY . /app/

# Set environment variable
ENV base_upload_dir=/app/upload_dir

# Expose FastAPI default port
EXPOSE 8000

