package datasources

import (
	"db-server/db"
	"db-server/models"
	"fmt"
	"net/http"

	"github.com/gin-gonic/gin"
)

func GetDataSource(ctx *gin.Context) {
	// Khởi tạo truy vấn
	query := db.DB

	// Mảng key của query parameters cần lọc
	queryParams := []string{"type"}

	// Thêm điều kiện vào truy vấn nếu giá trị không rỗng
	for _, key := range queryParams {
		value := ctx.Query(key)
		if value != "" {
			query = query.Where(fmt.Sprintf("%s = ?", key), value)
		}
	}

	// Thực hiện truy vấn để lấy danh sách người dùng
	var users []models.Datasource
	result := query.Find(&users)

	if result.Error != nil {
		ctx.JSON(http.StatusInternalServerError, gin.H{"message": "Có lỗi xảy ra, vui lòng thử lại sau."})
		return
	}

	ctx.JSON(http.StatusOK, gin.H{"data": users})
}

func CreateDataSource(ctx *gin.Context) {
	var user models.Datasource

	if err := ctx.ShouldBindJSON(&user); err != nil {
		ctx.JSON(http.StatusBadRequest, gin.H{"message": "Thông tin yêu cầu không hợp lệ."})
		return
	}

	result := db.DB.Create(&user)
	if result.Error != nil {
		ctx.JSON(http.StatusInternalServerError, gin.H{"message": "Có lỗi xảy ra, vui lòng thử lại sau."})
		return
	}

	ctx.JSON(http.StatusOK, gin.H{"data": user})
}

func UpdateDataSource(ctx *gin.Context) {
	id := ctx.Param("id")

	var updatedData models.Datasource

	if err := ctx.ShouldBindJSON(&updatedData); err != nil {
		ctx.JSON(http.StatusBadRequest, gin.H{"message": "Thông tin yêu cầu không hợp lệ."})
		return
	}

	// Cập nhật chỉ các trường cần thiết
	result := db.DB.Model(&models.Datasource{}).Where("id = ?", id).Select("Name", "Password").Updates(&updatedData)

	if result.Error != nil || result.RowsAffected == 0 {
		ctx.JSON(http.StatusNotFound, gin.H{"message": "Không tìm thấy người dùng."})
		return
	}

	ctx.JSON(http.StatusOK, gin.H{"message": "Cập nhật thông tin người dùng thành công"})
}

func DeleteDataSource(ctx *gin.Context) {
	id := ctx.Param("id")

	result := db.DB.Where("id = ?", id).Delete(&models.Datasource{})

	if result.Error != nil || result.RowsAffected == 0 {
		ctx.JSON(http.StatusNotFound, gin.H{"message": "Không tìm thấy người dùng."})
		return
	}

	ctx.JSON(http.StatusOK, gin.H{"message": "Xóa người dùng thành công"})
}
