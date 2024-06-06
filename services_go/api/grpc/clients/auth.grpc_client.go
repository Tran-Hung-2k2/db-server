package grpc_clients

import (
	"db-server/pb"

	"google.golang.org/grpc"
)

var AuthGRPCClient pb.AuthServiceClient

func StartAuthGrpcClient(server string) (*grpc.ClientConn, error) {
	// Kết nối đến microservice khác
	conn, err := grpc.Dial(server, grpc.WithInsecure())

	// Tạo một gRPC client
	AuthGRPCClient = pb.NewAuthServiceClient(conn)

	return conn, err
}
