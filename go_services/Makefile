# Variables
PROTO_DIR := ./proto
PB_DIR := ./pb

# Commands
PROTOC := protoc
GO_OUT := --go_out=$(PB_DIR) --go_opt=paths=source_relative
GO_GRPC_OUT := --go-grpc_out=$(PB_DIR) --go-grpc_opt=paths=source_relative

# Find all .proto files in the PROTO_DIR
PROTO_FILES := $(wildcard $(PROTO_DIR)/*.proto)

# Default target
all: clean proto

# Generate Go files from .proto files
proto: $(PB_DIR) $(PROTO_FILES)
	$(PROTOC) $(GO_OUT) $(GO_GRPC_OUT) -I$(PROTO_DIR) $(PROTO_FILES)

# Create PB_DIR if it doesn't exist
$(PB_DIR):
	mkdir -p $(PB_DIR)

# Clean up generated files
clean:
	rm -rf $(PB_DIR)/*

auth: 
	go run cmd/auth/main.go

users: 
	go run cmd/users/main.go

datasources: 
	go run cmd/datasources/main.go

swagger:
	swag init -g ./cmd/users/main.go -o docs

build:
	docker-compose build --parallel

docker:
	docker-compose up -d

rebuild:
	docker-compose up -d --build

nginx:
	docker-compose restart nginx

.PHONY: all proto clean

