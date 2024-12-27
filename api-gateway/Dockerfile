# Use official NGINX image as base
FROM nginx:latest

# Copy the custom NGINX configuration file into the container
COPY nginx.conf /etc/nginx/nginx.conf

# Copy frontend HTML file
COPY background.png /usr/share/nginx/html/background.png
COPY index.html /usr/share/nginx/html/index.html


# Expose port 80 for the web server
EXPOSE 80
