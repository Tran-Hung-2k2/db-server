package utils

import (
	"github.com/gin-gonic/gin"
)

func MakeResponse(message string, data interface{}, detail string) gin.H {
	// Chuyển đổi data thành một bản đồ
	dataMap, ok := data.(map[string]interface{})

	var response gin.H
	if !ok {
		response = gin.H{"message": message, "detail": detail, "data": data}
	} else {
		response = gin.H{"message": message, "detail": detail}
		for key, value := range dataMap {
			response[key] = value
		}
	}

	return response
}
