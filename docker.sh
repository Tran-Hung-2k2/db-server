#!/bin/bash

# Define an array with Docker Compose file names and corresponding image names
compose_files=(
# "compose-file-name:image-name"
  # "docker-compose-nginx.yml:db-server-nginx"
  "docker-compose-notebooks.yml:db-server-notebooks"
  # "docker-compose-auth.yml:db-server-auth"
  # "docker-compose-channels.yml:db-server-channels"
  # "docker-compose-datamarts.yml:db-server-data_marts"
)

# Create directory to store Docker images
rm -rf docker_images
mkdir -p docker_images

# Loop through all items in the array
for item in "${compose_files[@]}"; do
  # Split item into compose file and image name
  IFS=':' read -r compose_file image_name <<< "$item"

  # Build Docker image using the compose file
  docker-compose -f "$compose_file" build

  # Save Docker image to tar file
  docker image save -o "docker_images/${image_name}.tar" "${image_name}:latest"
done

# Transfer saved images to remote server
scp docker_images/* 139:/home/vht/duonghdt/db-server/docker_images