package users

import (
	"db-server/db"
	"db-server/models"
	"errors"
	"fmt"
	"net/http"

	"github.com/gin-gonic/gin"
	uuid "github.com/satori/go.uuid"
	"gorm.io/gorm"
)

func GetChannel(ctx *gin.Context) {
	// Khởi tạo truy vấn
	query := db.DB

	// Mảng key của query parameters cần lọc
	queryParams := []string{"id", "user_id", "type"}

	// Thêm điều kiện vào truy vấn nếu giá trị không rỗng
	for _, key := range queryParams {
		value := ctx.Query(key)
		if value != "" {
			query = query.Where(fmt.Sprintf("%s = ?", key), value)
		}
	}

	// Thực hiện truy vấn để lấy danh sách channel
	var records []models.Channel
	result := query.Find(&records)

	if result.Error != nil {
		ctx.JSON(http.StatusInternalServerError, gin.H{"message": "Có lỗi xảy ra, vui lòng thử lại sau."})
		return
	}

	ctx.JSON(http.StatusOK, gin.H{"data": records})
}

func CreateChannel(ctx *gin.Context) {
	var record models.Channel

	if err := ctx.ShouldBindJSON(&record); err != nil {
		ctx.JSON(http.StatusBadRequest, gin.H{"message": "Thông tin yêu cầu không hợp lệ."})
		return
	}

	record.UserID = uuid.FromStringOrNil(ctx.GetString("id"))

	result := db.DB.Create(&record)
	if result.Error != nil {
		ctx.JSON(http.StatusInternalServerError, gin.H{"message": "Có lỗi xảy ra, vui lòng thử lại sau."})
		return
	}
	fmt.Println(record)

	ctx.JSON(http.StatusOK, gin.H{"data": record})
}

func UpdateChannel(ctx *gin.Context) {
	id := ctx.Param("id")

	var record models.Channel

	if err := ctx.ShouldBindJSON(&record); err != nil {
		ctx.JSON(http.StatusBadRequest, gin.H{"message": "Thông tin yêu cầu không hợp lệ."})
		return
	}

	// Kiểm tra user_id trước khi update
	existingRecord := models.Channel{}
	result := db.DB.Where("id = ?", id).First(&existingRecord)
	if result.Error != nil {
		if errors.Is(result.Error, gorm.ErrRecordNotFound) {
			ctx.JSON(http.StatusNotFound, gin.H{"message": "Không tìm thấy channel."})
			return
		}
		ctx.JSON(http.StatusInternalServerError, gin.H{"message": "Có lỗi xảy ra, vui lòng thử lại sau."})
		return
	}

	if existingRecord.UserID != uuid.FromStringOrNil(ctx.GetString("id")) {
		ctx.JSON(http.StatusBadRequest, gin.H{"message": "Bạn không có quyền truy cập tài nguyên này."})
		return
	}

	// Cập nhật chỉ các trường cần thiết
	db.DB.Model(&models.Channel{}).Where("id = ?", id).Select("Name", "Config").Updates(&record)

	ctx.JSON(http.StatusOK, gin.H{"message": "Cập nhật thông tin channel thành công", "data": record})
}

func DeleteChannel(ctx *gin.Context) {
	id := ctx.Param("id")

	result := db.DB.Where("id = ?", id).Delete(&models.Channel{})

	if result.Error != nil || result.RowsAffected == 0 {
		ctx.JSON(http.StatusNotFound, gin.H{"message": "Không tìm thấy channel."})
		return
	}

	ctx.JSON(http.StatusOK, gin.H{"message": "Xóa channel thành công"})
}
