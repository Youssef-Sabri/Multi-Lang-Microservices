# Base image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy shared requirements
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Preload the pre-trained model for translation (optional, if needed for both services)
RUN python -c "from transformers import pipeline; pipeline('translation_ar_to_en', model='Helsinki-NLP/opus-mt-ar-en')"

# Copy application code
COPY . /app/ar2en_service

# Expose FastAPI port (only needed for FastAPI container)
EXPOSE 8001
