package users

import (
	"db-server/docs"
	"db-server/middlewares"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"

	swaggerFiles "github.com/swaggo/files"
	ginSwagger "github.com/swaggo/gin-swagger"
)

// InitRouter khởi tạo và cấu hình router của ứng dụng.
func InitRouter() *gin.Engine {
	// Tạo một đối tượng gin mặc định
	r := gin.Default()

	// Áp dụng middleware CORS vào router
	r.Use(configCORSMiddleware())

	basePath := "/api/v1/users"

	// Tạo nhóm route
	v1 := r.Group(basePath)
	{
		v1.GET("/", middlewares.VerifyAdmin(), GetUser)
		v1.POST("/", middlewares.VerifyAdmin(), CreateUser)
		v1.PUT("/:id", middlewares.VerifyAdmin(), UpdateUser)
		v1.DELETE("/:id", middlewares.VerifyAdmin(), DeleteUser)
	}

	// Cấu hình thông tin Swagger
	docs.SwaggerInfo.BasePath = basePath
	r.GET("/swagger/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))

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
