# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy only requirements first
COPY requirements.txt /app/requirements.txt

# Install dependencies first, leveraging Docker's caching
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy download_models.py and run it before copying the rest of the files
COPY download_models.py /app/download_models.py
RUN python /app/download_models.py

# Copy the rest of the application files (this won't affect the model download step)
COPY . /app

# Expose the port for Flask (8002)
EXPOSE 8002
