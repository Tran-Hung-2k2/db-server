package grpc_servers

import (
	"context"
	"db-server/db"
	"db-server/models"
	"db-server/pb"
	"errors"
	"log"
	"net"

	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
	"gorm.io/gorm"
)

type ChannelServiceServer struct {
	pb.ChannelServiceServer
}

func (server *ChannelServiceServer) GetChannel(ctx context.Context, req *pb.GetChannelRequest) (*pb.GetChannelResponse, error) {
	id := req.GetId()

	data := models.Channel{}
	result := db.DB.Where("id = ?", id).First(&data)

	if result.Error != nil {
		if errors.Is(result.Error, gorm.ErrRecordNotFound) {
			return nil, status.Errorf(codes.NotFound, "Không tìm thấy channel.")
		}
		return nil, status.Errorf(codes.Internal, "Có lỗi xảy ra, vui lòng thử lại sau")
	}

	// Trả về phản hồi thành công nếu không có lỗi
	return &pb.GetChannelResponse{
		Data: map[string]string{
			"id":      data.ID.String(),
			"user_id": data.UserID.String(),
			"name":    data.Name,
			"type":    string(data.Type),
			"config":  string(data.Config),
		},
	}, nil
}

func StartChannelGrpcServer(host string) {
	lis, err := net.Listen("tcp", host)
	if err != nil {
		log.Fatalf("Failed to listen: %v", err)
	}

	// Tạo grpc server
	grpcServer := grpc.NewServer()

	// Đăng ký service với server
	pb.RegisterChannelServiceServer(grpcServer, &ChannelServiceServer{})

	// Chạy server trong goroutine
	go func() {
		if err := grpcServer.Serve(lis); err != nil {
			log.Fatalf("Failed to serve: %v", err)
		}
	}()
}
