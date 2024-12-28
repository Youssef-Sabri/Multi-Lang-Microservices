# English to Arabic Translation Service (en2ar_service)

## Overview
The English to Arabic Translation Service (`en2ar_service`) is a microservice responsible for translating text from English to Arabic in real-time. This service is part of the cloud-native platform designed for real-time translation and text summarization.

## Contents
- `en2ar_service.py`: Main script for the translation service.
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
2. Navigate to the `en2ar_service` folder:
    ```bash
    cd microservices-translation-summarization-platform/en2ar_service
    ```
3. Install the required Python libraries:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
To start the English to Arabic Translation Service, execute the following command:
```bash
python en2ar_service.py
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
  name: en2ar_translation_service
  port: 5004
  translator_model: "Helsinki-NLP/opus-mt-en-ar"
```
## 📦 Installation
1. Clone the repository:
   ```bash
   https://github.com/Youssef-Sabri/cse363-cloud-computing-Cloud_warriors-Multi-Lang-Microservices/tree/main/en2ar_service
