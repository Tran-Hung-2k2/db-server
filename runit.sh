#!/bin/bash

# Pull the latest changes from Git
echo "Pulling latest changes from Git..."
git pull
if [ $? -ne 0 ]; then
    echo "Git pull failed. Exiting."
    exit 1
fi

# Build Docker services in parallel
echo "Building Docker services..."
docker-compose build --parallel
if [ $? -ne 0 ]; then
    echo "Docker Compose build failed. Exiting."
    exit 1
fi

# Bring up the Docker containers
echo "Starting Docker containers..."
docker-compose up -d
if [ $? -ne 0 ]; then
    echo "Docker Compose up failed. Exiting."
    exit 1
fi

# Restart the NGINX container
echo "Restarting NGINX container..."
docker-compose restart nginx
if [ $? -ne 0 ]; then
    echo "Failed to restart NGINX container. Exiting."
    exit 1
fi

echo "Done."
