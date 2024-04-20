package utils

import (
	"db-server/constants"
	"errors"

	"github.com/gin-gonic/gin"
	"github.com/mitchellh/mapstructure"
)

func GetDataFromRequest(ctx *gin.Context, data interface{}) error {
	// Get the validated data from the context and perform a type assertion
	validData, exists := ctx.Get(constants.DATA_CTX_KEY)
	if !exists {
		return errors.New("not found valid data in context")
	}

	err := mapstructure.Decode(validData, &data)
	if err != nil {
		return err
	}

	return nil
}
