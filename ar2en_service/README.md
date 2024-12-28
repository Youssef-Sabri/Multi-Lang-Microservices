# Arabic to English Translation Service (ar2en_service)

## Overview
The Arabic to English Translation Service (`ar2en_service`) is a microservice responsible for translating text from Arabic to English in real-time. This service is part of the cloud-native platform designed for real-time translation and text summarization.

## Contents
- `ar2en_service.py`: Main script for the translation service.
- `requirements.txt`: Lists the Python dependencies required for the service.
- `config.yaml`: Configuration file for setting up the service parameters.

## Installation and Requirements

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/Youssef-Sabri/cse363-cloud-computing-Cloud_warriors-Multi-Lang-Microservices.git
    ```
2. Navigate to the `ar2en_service` folder:
    ```bash
    cd cse363-cloud-computing-Cloud_warriors-Multi-Lang-Microservices/ar2en_service
    ```
3. Install the required Python libraries:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
To start the Arabic to English Translation Service, execute the following command:
```bash
python ar2en_service.py
```

## Dependencies
The `requirements.txt` file includes the necessary dependencies for the translation service. Here are the primary libraries:
- FastAPI
- Uvicorn
- Translation libraries (e.g., `transformers`, `torch`)

## Configuration
Update `config.yaml` to configure the service parameters. Example configuration:
```yaml
service:
  name: ar2en_translation_service
  port: 5003
  translator_model: "Helsinki-NLP/opus-mt-ar-en"
```

## 📦 Installation
1. Clone the repository:
   ```bash
   https://github.com/Youssef-Sabri/cse363-cloud-computing-Cloud_warriors-Multi-Lang-Microservices/tree/main/ar2en_service
