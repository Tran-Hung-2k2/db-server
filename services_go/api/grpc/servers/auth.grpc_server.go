package grpc_servers

import (
	"context"
	"db-server/pb"
	"db-server/utils"
	"log"
	"net"

	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

type AuthServiceServer struct {
	pb.UnimplementedAuthServiceServer
}

func (server *AuthServiceServer) VerifyRole(ctx context.Context, req *pb.VerifyRequest) (*pb.VerifyResponse, error) {
	accessToken := req.GetToken()
	roles := req.GetRoles()
	// utils.Info.Println(accessToken)

	data, err := utils.VerifyAccessToken(accessToken, []string{"id", "role"})
	if err != nil {
		utils.Info.Println("Xác thực thất bại do thông tin xác thất sai hoặc đã hết hạn.")
		return nil, status.Errorf(codes.Unauthenticated, "Xác thực thất bại do thông tin xác thất sai hoặc đã hết hạn.")
	}

	// Kiểm tra xem role có nằm trong danh sách roles không
	if !utils.Contains(data["role"], roles) {
		utils.Info.Println("Bạn không có quyền truy cập vào tài nguyên này.")
		return nil, status.Errorf(codes.PermissionDenied, "Bạn không có quyền truy cập vào tài nguyên này.")
	}

	// Trả về phản hồi thành công nếu không có lỗi
	return &pb.VerifyResponse{
		Data: data,
	}, nil
}

func StartAuthGrpcServer(host string) {
	lis, err := net.Listen("tcp", host)
	if err != nil {
		log.Fatalf("Failed to listen: %v", err)
	}

	// Tạo grpc server
	grpcServer := grpc.NewServer()

	// Đăng ký service với server
	pb.RegisterAuthServiceServer(grpcServer, &AuthServiceServer{})

	// Chạy server trong goroutine
	go func() {
		if err := grpcServer.Serve(lis); err != nil {
			log.Fatalf("Failed to serve: %v", err)
		}
	}()
}
