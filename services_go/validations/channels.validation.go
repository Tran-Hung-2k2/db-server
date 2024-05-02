package validations

import (
	"db-server/schemas"

	"github.com/gin-gonic/gin"
)

func GetChannel() gin.HandlerFunc {
	return func(ctx *gin.Context) {
		errorMessages := map[string]string{}

		// Validate the data
		if err := QueryValidation(ctx, &schemas.GetChannelRequest{}, errorMessages); err != nil {
			ctx.Abort()
			return
		}

		ctx.Next()
	}
}

func CreateChannel() gin.HandlerFunc {
	return func(ctx *gin.Context) {
		errorMessages := map[string]string{}

		// Validate the data
		if err := BodyValidation(ctx, &schemas.CreateChannelRequest{}, errorMessages); err != nil {
			ctx.Abort()
			return
		}

		ctx.Next()
	}
}

func UpdateChannel() gin.HandlerFunc {
	return func(ctx *gin.Context) {
		errorMessages := map[string]string{}

		// Validate the data
		if err := BodyValidation(ctx, &schemas.UpdateChannelRequest{}, errorMessages); err != nil {
			ctx.Abort()
			return
		}

		ctx.Next()
	}
}
