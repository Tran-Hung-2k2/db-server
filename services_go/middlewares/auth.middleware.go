package middlewares

import (
	"context"
	grpc_clients "db-server/api/grpc/clients"
	"db-server/pb"
	"net/http"

	"github.com/gin-gonic/gin"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

func VerifyRole(roles []string) gin.HandlerFunc {
	return func(ctx *gin.Context) {
		accessToken, _ := ctx.Cookie("access_token")

		response, err := grpc_clients.AuthGRPCClient.VerifyRole(context.Background(), &pb.VerifyRequest{Token: accessToken, Roles: roles})

		if err != nil {
			// Kiểm tra xem lỗi có phải là lỗi của gRPC không
			if st, ok := status.FromError(err); ok {
				// Lấy mã lỗi và thông báo
				grpcCode := st.Code()
				message := st.Message()

				// Sử dụng mã lỗi và thông báo để xử lý
				switch grpcCode {
				case codes.Unauthenticated:
					ctx.JSON(http.StatusUnauthorized, gin.H{"message": message})
				case codes.PermissionDenied:
					ctx.JSON(http.StatusForbidden, gin.H{"message": message})
				default:
					ctx.JSON(http.StatusInternalServerError, gin.H{"message": "Có lỗi xảy ra, vui lòng thử lại sau."})
				}

				ctx.Abort()
				return
			}
		}

		// Đặt dữ liệu vào Context
		ctx.Set("id", response.Data["id"])
		ctx.Set("role", response.Data["role"])

		// Tiếp tục xử lý ở các middleware và controller tiếp theo
		ctx.Next()
	}
}

func VerifyAdmin() gin.HandlerFunc {
	return VerifyRole([]string{"admin"})
}

func VerifyUser() gin.HandlerFunc {
	return VerifyRole([]string{"user"})
}

func VerifyAll() gin.HandlerFunc {
	return VerifyRole([]string{"user", "admin"})
}
