# Base image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy shared requirements
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Preload the pre-trained model for translation (optional, if needed for both services)
RUN python -c "from transformers import pipeline; pipeline('translation_en_to_ar', model='Helsinki-NLP/opus-mt-en-ar')"

# Copy application code
COPY . /app/en2ar_service

# Expose FastAPI port (only needed for FastAPI container)
EXPOSE 8000
