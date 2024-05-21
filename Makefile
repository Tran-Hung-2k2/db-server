# Variables
PROTO_DIR := ./proto
GO_PB_DIR := ./services_go/pb
PYTHON_PB_DIR := ./services_python/pb

# Find all .proto files in the PROTO_DIR
PROTO_FILES := $(wildcard $(PROTO_DIR)/*.proto)

# Default target
all: proto

# Generate Go and Py files from .proto files
proto: $(GO_PB_DIR) $(PYTHON_PB_DIR) $(PROTO_FILES)
	rm -rf $(GO_PB_DIR)/*
	rm -rf $(PYTHON_PB_DIR)/*
	protoc --go_out=$(GO_PB_DIR) --go_opt=paths=source_relative --go-grpc_out=$(GO_PB_DIR) --go-grpc_opt=paths=source_relative -I $(PROTO_DIR) $(PROTO_FILES)
	python -m grpc_tools.protoc  --python_out=$(PYTHON_PB_DIR) --grpc_python_out=$(PYTHON_PB_DIR) -I $(PROTO_DIR) $(PROTO_FILES)

# Create PB_DIR if it doesn't exist
$(GO_PB_DIR):
	mkdir -p $(GO_PB_DIR)

$(PYTHON_PB_DIR):
	mkdir -p $(PYTHON_PB_DIR)

# Golang swagger
swagger:
	swag init -g ./services_go/cmd/users/main.go -o services_go/docs

# Buil docker compose
docker-compose:
	docker-compose up -d --build

# Python requirement
imreq:
	pip install -r services_python/datasets_service/requirements.txt

exreq:
	pip freeze > services_python/datasets_service/requirements.txt

# Run Service
ifeq ($(OS),Windows_NT)
PYTHON=python
else
PYTHON=python3
endif

# Run Service
magesrv:
	$(PYTHON) services_python/mage_service/app/main.py

setsrv:
	$(PYTHON) services_python/datasets_service/app/main.py

authsrv: 
	cd services_go && go run cmd/auth/main.go

martsrv: 
	cd services_go && go run cmd/data_marts/main.go

channelsrv: 
	cd services_go && go run cmd/channels/main.go

usersrv: 
	cd services_go && go run cmd/users/main.go

