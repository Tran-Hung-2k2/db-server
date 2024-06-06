package utils

import (
	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

var ALLOW_ORIGIN = GetEnv("ALLOW_ORIGIN", "http://localhost:5173")

func ConfigCORSMiddleware() gin.HandlerFunc {
	// Cấu hình middleware CORS
	config := cors.DefaultConfig()
	config.AllowAllOrigins = false
	config.AllowOrigins = append(config.AllowOrigins, ALLOW_ORIGIN)
	// config.AllowOrigins = []string{ALLOW_ORIGIN}
	config.AllowMethods = []string{"GET", "HEAD", "OPTIONS", "PUT", "PATCH", "POST", "DELETE"}
	config.AllowHeaders = []string{"Origin", "Content-Length", "Content-Type", "Access-Control-Allow-Headers", "Authorization", "Set-Cookie"}
	config.AllowCredentials = true
	return cors.New(config)
}
