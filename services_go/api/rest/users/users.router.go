package users

import (
	"db-server/docs"
	"db-server/middlewares"
	"db-server/utils"
	"db-server/validations"

	"github.com/gin-gonic/gin"

	swaggerFiles "github.com/swaggo/files"
	ginSwagger "github.com/swaggo/gin-swagger"
)

// InitRouter khởi tạo và cấu hình router của ứng dụng.
func InitRouter() *gin.Engine {
	// Tạo một đối tượng gin mặc định
	r := gin.Default()

	// Áp dụng middleware CORS vào router
	r.Use(utils.ConfigCORSMiddleware())

	basePath := "/api/users"

	// Tạo nhóm route
	v1 := r.Group(basePath)
	{
		v1.GET("/", validations.GetUser(), middlewares.VerifyAdmin(), GetUser)
		v1.DELETE("/:id", middlewares.VerifyAdmin(), DeleteUser)
	}

	// Cấu hình thông tin Swagger
	docs.SwaggerInfo.BasePath = basePath
	r.GET("/swagger/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))

	return r
}
