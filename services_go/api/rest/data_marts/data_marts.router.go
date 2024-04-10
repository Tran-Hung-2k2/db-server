package users

import (
	"db-server/middlewares"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

// InitRouter khởi tạo và cấu hình router của ứng dụng.
func InitRouter() *gin.Engine {
	// Tạo một đối tượng gin mặc định
	r := gin.Default()

	// Áp dụng middleware CORS vào router
	r.Use(configCORSMiddleware())

	basePathMart := "/api/data_marts"
	basePathSet := "/api/datasets"

	// Tạo nhóm route
	v1_mart := r.Group(basePathMart)
	{
		v1_mart.GET("/", middlewares.VerifyUser(), GetDataMart)
		v1_mart.POST("/", middlewares.VerifyUser(), CreateDataMart)
		v1_mart.PUT("/:id", middlewares.VerifyUser(), UpdateDataMart)
		v1_mart.DELETE("/:id", middlewares.VerifyUser(), DeleteDataMart)
	}

	v1_set := r.Group(basePathSet)
	{
		v1_set.GET("/", middlewares.VerifyUser(), GetDataMart)
		v1_set.POST("/", middlewares.VerifyUser(), CreateDataMart)
		v1_set.PUT("/:id", middlewares.VerifyUser(), UpdateDataMart)
		v1_set.DELETE("/:id", middlewares.VerifyUser(), DeleteDataMart)
	}

	return r
}

func configCORSMiddleware() gin.HandlerFunc {
	// Cấu hình middleware CORS
	config := cors.DefaultConfig()
	config.AllowAllOrigins = true
	config.AllowMethods = []string{"GET", "POST", "OPTIONS", "PATCH", "DELETE", "PUT"}
	config.AllowHeaders = []string{"Origin", "Content-Length", "Content-Type"}
	return cors.New(config)
}
