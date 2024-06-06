package validations

import (
	"db-server/schemas"

	"github.com/gin-gonic/gin"
)

func GetUser() gin.HandlerFunc {
	return func(ctx *gin.Context) {
		errorMessages := map[string]string{
			"'email' tag": "Định dạng Email không hợp lệ.",
		}

		// Validate the data
		if err := QueryValidation(ctx, &schemas.GetUserRequest{}, errorMessages); err != nil {
			ctx.Abort()
			return
		}

		ctx.Next()
	}
}
