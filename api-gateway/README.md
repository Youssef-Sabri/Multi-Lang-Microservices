# API Gateway

## Overview
The API Gateway is responsible for routing requests to the appropriate backend microservices, handling authentication, and aggregating responses. It acts as a single entry point for clients to interact with the various services of the cloud-native platform.

## Contents
- `gateway.py`: Main script for the API Gateway.
- `config.yaml`: Configuration file for setting up routes and services.
- `requirements.txt`: Lists the Python dependencies required for the API Gateway.

## Usage
To start the API Gateway, navigate to this folder and execute the following commands:
```bash
pip install -r requirements.txt
python gateway.py
```
### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/Youssef-Sabri/cse363-cloud-computing-Cloud_warriors-Multi-Lang-Microservices.git
    ```
2. Navigate to the `api-gateway` folder:
    ```bash
    cd cse363-cloud-computing-Cloud_warriors-Multi-Lang-Microservices/api-gateway
    ```

## Dependencies
- Python 3.8 or higher
- Libraries listed in `requirements.txt`

## Configuration
Update `config.yaml` to configure the routes and services. Example configuration:
```yaml
routes:
  - path: /translate
    service: translation_service
  - path: /summarize
    service: summarization_service
services:
  translation_service:
    url: http://localhost:5001
  summarization_service:
    url: http://localhost:5002
```

