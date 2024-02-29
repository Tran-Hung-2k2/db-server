# Stage 1: Build the Go binary
FROM golang:1.22.0 AS builder

WORKDIR /app

# Copy the entire project
# Make sure your Docker build context is the project root
COPY . .

# Download dependencies
RUN go mod download

# Build the application
# Adjust the path to where your main.go is located
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main cmd/auth/main.go

# Stage 2: Create a minimal image with only the compiled binary
FROM alpine:latest

WORKDIR /root/

# Copy the binary from the builder stage
COPY --from=builder /app/main .

EXPOSE 8080

CMD ["./main"]
