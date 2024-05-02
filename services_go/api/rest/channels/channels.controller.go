package users

import (
	"db-server/constants"
	"db-server/db"
	"db-server/models"
	"db-server/utils"
	"errors"
	"fmt"
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	uuid "github.com/satori/go.uuid"
	"gorm.io/gorm"
)

var LIMIT_RECORD = utils.GetEnv("LIMIT_RECORD", "50")

func GetChannel(ctx *gin.Context) {
	// Khởi tạo truy vấn
	var query *gorm.DB
	if ctx.GetString(constants.USER_ROLE_KEY) != string(constants.Admin) {
		query, _ = utils.AddQueryData(ctx, db.DB, map[string]interface{}{
			"user_id": ctx.GetString(constants.USER_ID_KEY),
		})
	} else {
		query, _ = utils.AddQueryData(ctx, db.DB, map[string]interface{}{})
	}

	// Get limit and skip from query parameters
	limit, _ := strconv.Atoi(ctx.DefaultQuery("limit", LIMIT_RECORD))
	skip, _ := strconv.Atoi(ctx.DefaultQuery("skip", "0"))

	// Get total count
	var total int64
	query.Model(&models.Channel{}).Count(&total)

	// Thực hiện truy vấn để lấy danh sách người dùng
	var records []models.Channel
	result := query.Limit(limit).Offset(skip).Find(&records)

	if result.Error != nil {
		ctx.JSON(http.StatusInternalServerError, utils.MakeResponse("Có lỗi xảy ra, vui lòng thử lại sau.", nil, result.Error.Error()))
		return
	}

	ctx.JSON(http.StatusOK, utils.MakeResponse("Lấy danh sách channel thành công.", gin.H{"data": records, "limit": limit, "skip": skip, "total": total}, ""))
}

func CreateChannel(ctx *gin.Context) {
	var record models.Channel
	if err := utils.GetBodyData(ctx, &record); err != nil {
		ctx.JSON(http.StatusBadRequest, utils.MakeResponse("Định dạng dữ liệu không hợp lệ.", nil, err.Error()))
		return
	}

	// Print the type of data
	fmt.Printf("Type of data: %T\n", record.Config)

	record.UserID = uuid.FromStringOrNil(ctx.GetString(constants.USER_ID_KEY))

	result := db.DB.Create(&record)
	if result.Error != nil {
		ctx.JSON(http.StatusInternalServerError, utils.MakeResponse("Có lỗi xảy ra, vui lòng thử lại sau.", nil, result.Error.Error()))
		return
	}
	ctx.JSON(http.StatusCreated, utils.MakeResponse("Tạo channel thành công.", record, ""))
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

	if existingRecord.UserID != uuid.FromStringOrNil(ctx.GetString(constants.USER_ID_KEY)) {
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

	if result.RowsAffected == 0 {
		ctx.JSON(http.StatusNotFound, utils.MakeResponse("Không tìm thấy channel.", nil, ""))
		return
	} else if result.Error != nil {
		ctx.JSON(http.StatusInternalServerError, utils.MakeResponse("Có lỗi xảy ra, vui lòng thử lại sau.", nil, result.Error.Error()))
		return
	}

	ctx.JSON(http.StatusOK, utils.MakeResponse("Xóa channel thành công.", nil, ""))
}
