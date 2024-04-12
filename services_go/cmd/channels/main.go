package main

import (
	grpc_clients "db-server/api/grpc/clients"
	grpc_servers "db-server/api/grpc/servers"
	restAPI "db-server/api/rest/channels"
	"db-server/db"
	"db-server/models"
	"db-server/utils"
	"log"

	"github.com/joho/godotenv"
)

func main() {
	godotenv.Load()
	restHost := utils.GetEnv("REST_HOST", "")
	restPort := utils.GetEnv("REST_PORT", "8084")
	grpcHost := utils.GetEnv("GRPC_HOST", ":50052")
	authGrpcServer := utils.GetEnv("AUTH_GRPC_SERVER", "127.0.0.1:50051")

	// Kết nối database
	db.ConnectToPostgres(&models.Channel{})

	// Chạy grpc server
	go grpc_servers.StartChannelGrpcServer(grpcHost)

	// Kết nối grpc
	conn, err := grpc_clients.StartAuthGrpcClient(authGrpcServer)
	if err != nil {
		log.Fatalf("Failed to connect: %v", err)
	}
	defer conn.Close()

	// Chạy server
	server := restAPI.InitRouter()
	server.Run(restHost + ":" + restPort)
}
