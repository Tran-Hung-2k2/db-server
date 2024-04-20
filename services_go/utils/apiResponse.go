package utils

import (
	"github.com/gin-gonic/gin"
)

func MakeResponse(message string, data interface{}, detail string) gin.H {
	response := gin.H{}

	response["message"] = message
	response["detail"] = detail
	response["data"] = data

	return response
}
