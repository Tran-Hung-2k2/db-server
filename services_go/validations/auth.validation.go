package validations

import (
	"db-server/schemas"

	"github.com/gin-gonic/gin"
)

func SignUp() gin.HandlerFunc {
	return func(ctx *gin.Context) {
		errorMessages := map[string]string{
			"'email' tag":             "Định dạng Email không hợp lệ.",
			"password of type string": "Mật khẩu phải có định dạng chuỗi.",
		}

		// Validate the data
		if err := BaseValidation(ctx, &schemas.SignUpRequest{}, errorMessages); err != nil {
			ctx.Abort()
			return
		}

		ctx.Next()
	}
}

func SignIn() gin.HandlerFunc {
	return func(ctx *gin.Context) {
		errorMessages := map[string]string{
			"'email' tag":             "Định dạng Email không hợp lệ.",
			"password of type string": "Mật khẩu phải có định dạng chuỗi.",
		}

		// Validate the data
		if err := BaseValidation(ctx, &schemas.SignInRequest{}, errorMessages); err != nil {
			ctx.Abort()
			return
		}

		ctx.Next()
	}
}
