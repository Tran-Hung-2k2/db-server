package utils

import (
	"github.com/gin-gonic/gin"
)

func MakeResponse(message string, data interface{}, detail string) gin.H {
	return gin.H{"message": message, "detail": detail, "data": data}
}
