# Stage 1: Build the Go binary
FROM golang:1.22.0 AS builder

# Set the working directory inside the container
WORKDIR /app

# Copy the entire project into the container
# Make sure your Docker build context is the project root
COPY . .

# Download dependencies using Go modules
RUN cd services_go && go mod download

# Build the application
# Adjust the path to where your main.go is located
RUN cd services_go/cmd/auth && CGO_ENABLED=0 GOOS=linux go build -o /app/main .

# Stage 2: Create a minimal image with only the compiled binary
FROM alpine:latest

# Set the working directory inside the container
WORKDIR /root/

# Copy the binary from the builder stage to the final image
COPY --from=builder /app/main .

# Expose the port that the application will run on
EXPOSE 8080

# Define the command to run the application
CMD ["./main"]
