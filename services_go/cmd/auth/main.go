package main

import (
	grpc_servers "db-server/api/grpc/servers"
	restAPI "db-server/api/rest/auth"
	"db-server/db"
	"db-server/models"
	"db-server/utils"

	"github.com/joho/godotenv"
)

func main() {
	godotenv.Load()
	restHost := utils.GetEnv("REST_HOST", "")
	restPort := utils.GetEnv("REST_PORT", "8081")
	grpcHost := utils.GetEnv("GRPC_HOST", ":50051")

	// Kết nối database
	db.ConnectToPostgres(&models.User{})

	// Chạy grpc server
	go grpc_servers.StartAuthGrpcServer(grpcHost)

	// Chạy rest server
	server := restAPI.InitRouter()
	server.Run(restHost + ":" + restPort)
}
