# Variables
PROTO_DIR := ./proto
PB_DIR := ./services_go/pb

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
	go run services_go/cmd/auth/main.go

users: 
	go run services_go/cmd/users/main.go

swagger:
	swag init -g ./services_go/cmd/users/main.go -o services_go/docs

docker:
	docker-compose up -d

build:
	docker-compose up -d --build

nginx:
	docker-compose restart nginx

data:
	uvicorn python_services.data_service.app.main:app --reload

import_req:
	pip install -r python_services/data_service/requirements.txt

export_req:
	pip freeze > python_services/data_service/requirements.txt

.PHONY: all proto clean

