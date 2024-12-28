API Gateway Project

This project is designed as a web application served using Nginx and packaged within a Docker container. It includes configurations and assets necessary to deploy and run the gateway efficiently.

Project Structure

api-gateway/
├── background.png    # Image asset used in the project
├── Dockerfile        # Docker configuration file
├── index.html        # Main HTML file for the front-end
├── nginx.conf        # Nginx server configuration

Features

Web Application: A static front-end provided by index.html.

Nginx Server: Configured via nginx.conf to handle requests efficiently.

Dockerized: Easily deployable using Docker.

Prerequisites

Docker installed on your system.

Getting Started

Clone the repository:

git clone <repository-url>
cd api-gateway

Build the Docker image:

docker build -t api-gateway .

Run the Docker container:

docker run -p 8080:80 api-gateway

Open your browser and navigate to http://localhost:8080 to view the application.

Configuration

Nginx:
The nginx.conf file is pre-configured for basic usage. Modify this file to adjust server settings.

Project Assets

background.png:
An image asset included in the project, which may be used in the front-end design.
---

## 📦 Installation
1. Clone the repository:
   ```bash
   https://github.com/salahezzt120/microservices-translation-summarization-platform.git
