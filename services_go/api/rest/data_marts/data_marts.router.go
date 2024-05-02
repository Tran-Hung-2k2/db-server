package users

import (
	"db-server/docs"
	"db-server/middlewares"
	"db-server/utils"

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

	basePath := "/api/data_marts"

	// Tạo nhóm route
	v1 := r.Group(basePath)
	{
		v1.GET("/", middlewares.VerifyAll(), GetDataMart)
		v1.POST("/", middlewares.VerifyUser(), CreateDataMart)
		v1.PATCH("/:id", middlewares.VerifyUser(), UpdateDataMart)
		v1.DELETE("/:id", middlewares.VerifyUser(), DeleteDataMart)
	}

	// Cấu hình thông tin Swagger
	docs.SwaggerInfo.BasePath = basePath
	r.GET("/swagger/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))

	return r
}
