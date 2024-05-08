package validations

import (
	"db-server/schemas"

	"github.com/gin-gonic/gin"
)

func GetDataMart() gin.HandlerFunc {
	return func(ctx *gin.Context) {
		errorMessages := map[string]string{}

		// Validate the data
		if err := QueryValidation(ctx, &schemas.GetDataMartRequest{}, errorMessages); err != nil {
			ctx.Abort()
			return
		}

		ctx.Next()
	}
}

func CreateDataMart() gin.HandlerFunc {
	return func(ctx *gin.Context) {
		errorMessages := map[string]string{}

		// Validate the data
		if err := BodyValidation(ctx, &schemas.CreateDataMartRequest{}, errorMessages); err != nil {
			ctx.Abort()
			return
		}

		ctx.Next()
	}
}

func UpdateDataMart() gin.HandlerFunc {
	return func(ctx *gin.Context) {
		errorMessages := map[string]string{}

		// Validate the data
		if err := BodyValidation(ctx, &schemas.UpdateDataMartRequest{}, errorMessages); err != nil {
			ctx.Abort()
			return
		}

		ctx.Next()
	}
}
