# Use the official NGINX image as a base
FROM nginx:latest

# Remove the default NGINX configuration file
RUN rm /etc/nginx/conf.d/default.conf

# Copy the custom configuration file from the current directory to the container
COPY nginx/nginx.conf /etc/nginx/conf.d

# Expose port 80
EXPOSE 80
