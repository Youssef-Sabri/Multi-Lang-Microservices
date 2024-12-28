# Text Summarization Service

## Overview
The Text Summarization Service is a microservice responsible for summarizing text in real-time. This service is part of the cloud-native platform designed for real-time translation and text summarization.

## Contents
- `summarization_service.py`: Main script for the summarization service.
- `requirements.txt`: Lists the Python dependencies required for the service.
- `config.yaml`: Configuration file for setting up the service parameters.

## Installation and Requirements

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/salahezzt120/microservices-translation-summarization-platform.git
    ```
2. Navigate to the `text-summarization-service` folder:
    ```bash
    cd microservices-translation-summarization-platform/text-summarization-service
    ```
3. Install the required Python libraries:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
To start the Text Summarization Service, execute the following command:
```bash
python summarization_service.py
```

## Dependencies
The `requirements.txt` file includes the necessary dependencies for the summarization service. Here are the primary libraries:
- FastAPI
- Uvicorn
- Summarization libraries (e.g., `transformers`, `torch`)

## Configuration
Update `config.yaml` to configure the service parameters. Example configuration:
```yaml
service:
  name: text_summarization_service
  port: 5005
  summarizer_model: "facebook/bart-large-cnn"
```
