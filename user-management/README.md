# User Management Service

## Overview
The User Management Service is a microservice responsible for managing user data, authentication, and authorization. This service is part of the cloud-native platform designed for real-time translation and text summarization.

## Contents
- `user_management_service.py`: Main script for the user management service.
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
2. Navigate to the `user-management` folder:
    ```bash
    cd microservices-translation-summarization-platform/user-management
    ```
3. Install the required Python libraries:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
To start the User Management Service, execute the following command:
```bash
python user_management_service.py
```

## Dependencies
The `requirements.txt` file includes the necessary dependencies for the user management service. Here are the primary libraries:
- FastAPI
- Uvicorn
- Databases (e.g., SQLAlchemy, PostgreSQL)

## Configuration
Update `config.yaml` to configure the service parameters. Example configuration:
```yaml
service:
  name: user_management_service
  port: 5006
database:
  url: "postgresql://username:password@localhost/dbname"
```


## 📦 Installation
1. Clone the repository:
   ```bash
   https://github.com/Youssef-Sabri/cse363-cloud-computing-Cloud_warriors-Multi-Lang-Microservices/tree/main/user-management
