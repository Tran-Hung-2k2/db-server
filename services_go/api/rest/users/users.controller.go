package users

import (
	"db-server/db"
	"db-server/models"
	"fmt"
	"net/http"

	"github.com/gin-gonic/gin"
)

func GetUser(ctx *gin.Context) {
	// Khởi tạo truy vấn
	query := db.DB

	// Mảng key của query parameters cần lọc
	queryParams := []string{"id", "email", "role"}

	// Thêm điều kiện vào truy vấn nếu giá trị không rỗng
	for _, key := range queryParams {
		value := ctx.Query(key)
		if value != "" {
			query = query.Where(fmt.Sprintf("%s = ?", key), value)
		}
	}

	// Thực hiện truy vấn để lấy danh sách người dùng
	var users []models.User
	result := query.Find(&users)

	if result.Error != nil {
		ctx.JSON(http.StatusInternalServerError, gin.H{"message": "Có lỗi xảy ra, vui lòng thử lại sau."})
		return
	}

	ctx.JSON(http.StatusOK, gin.H{"data": users})
}

func CreateUser(ctx *gin.Context) {
	var user models.User

	if err := ctx.ShouldBindJSON(&user); err != nil {
		ctx.JSON(http.StatusBadRequest, gin.H{"message": "Thông tin yêu cầu không hợp lệ."})
		return
	}

	// Mã hóa mật khẩu của user
	user.HashPassword()

	result := db.DB.Create(&user)
	if result.Error != nil {
		ctx.JSON(http.StatusInternalServerError, gin.H{"message": "Có lỗi xảy ra, vui lòng thử lại sau."})
		return
	}

	ctx.JSON(http.StatusOK, gin.H{"data": user})
}

func UpdateUser(ctx *gin.Context) {
	id := ctx.Param("id")

	var updatedUser models.User

	if err := ctx.ShouldBindJSON(&updatedUser); err != nil {
		ctx.JSON(http.StatusBadRequest, gin.H{"message": "Thông tin yêu cầu không hợp lệ."})
		return
	}

	// Cập nhật chỉ các trường cần thiết
	result := db.DB.Model(&models.User{}).Where("id = ?", id).Select("Name", "Password").Updates(&updatedUser)

	if result.Error != nil || result.RowsAffected == 0 {
		ctx.JSON(http.StatusNotFound, gin.H{"message": "Không tìm thấy người dùng."})
		return
	}

	ctx.JSON(http.StatusOK, gin.H{"message": "Cập nhật thông tin người dùng thành công"})
}

func DeleteUser(ctx *gin.Context) {
	id := ctx.Param("id")

	result := db.DB.Where("id = ?", id).Delete(&models.User{})

	if result.Error != nil || result.RowsAffected == 0 {
		ctx.JSON(http.StatusNotFound, gin.H{"message": "Không tìm thấy người dùng."})
		return
	}

	ctx.JSON(http.StatusOK, gin.H{"message": "Xóa người dùng thành công"})
}
