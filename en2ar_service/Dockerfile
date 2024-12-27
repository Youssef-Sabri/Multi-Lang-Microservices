# Use the official Python slim image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY en2ar_service/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download the Hugging Face model
RUN python -c "from transformers import pipeline; pipeline('translation_en_to_ar', model='Helsinki-NLP/opus-mt-en-ar')"

# Copy the application code
COPY en2ar_service/ ./en2ar_service

# Expose the default port for FastAPI
EXPOSE 8000

# Command to run the app
CMD ["uvicorn", "en2ar_service.main:app", "--host", "0.0.0.0", "--port", "8000"]
