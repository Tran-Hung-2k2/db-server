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

func GetChannelDistinctValues(ctx *gin.Context) {
	field := ctx.DefaultQuery("field", "")

	if field == "" {
		ctx.JSON(http.StatusOK, utils.MakeResponse("Lấy danh sách giá trị thành công.", nil, ""))
		return
	}

	var records []string
	result := db.DB.Model(&models.Channel{}).Distinct(field).Pluck(field, &records)

	if result.Error != nil {
		ctx.JSON(http.StatusInternalServerError, utils.MakeResponse("Có lỗi xảy ra, vui lòng thử lại sau.", nil, result.Error.Error()))
		return
	}

	ctx.JSON(http.StatusOK, utils.MakeResponse("Lấy danh sách giá trị thành công.", records, ""))
}

func GetChannel(ctx *gin.Context) {
	// Khởi tạo truy vấn
	var query *gorm.DB
	if ctx.GetString(constants.USER_ROLE_KEY) != constants.ADMIN {
		query, _ = utils.AddQueryData(ctx, db.DB, map[string]interface{}{
			"user_id": ctx.GetString(constants.USER_ID_KEY),
		})
	} else {
		query, _ = utils.AddQueryData(ctx, db.DB, map[string]interface{}{})
	}

	// Get limit and skip from query parameters
	limit, _ := strconv.Atoi(ctx.DefaultQuery("limit", LIMIT_RECORD))
	skip, _ := strconv.Atoi(ctx.DefaultQuery("skip", "0"))
	sort_by := ctx.DefaultQuery("sort_by", "created_at")
	sort_dim := ctx.DefaultQuery("sort_dim", "desc")
	name := ctx.DefaultQuery("name", "")

	if !utils.Contains(sort_by, []string{"id", "created_at", "updated_at", "user_id", "name", "type", "description"}) {
		sort_by = "created_at"
	}
	if !utils.Contains(sort_dim, []string{"asc", "desc"}) {
		sort_dim = "desc"
	}

	// Get total count
	var total int64
	query.Model(&models.Channel{}).Where("LOWER(name) LIKE LOWER(?)", "%"+name+"%").Count(&total)

	var records []models.Channel
	result := query.Where("LOWER(name) LIKE LOWER(?)", "%"+name+"%").Order(fmt.Sprintf("%s %s", sort_by, sort_dim)).Limit(limit).Offset(skip).Find(&records)

	if result.Error != nil {
		ctx.JSON(http.StatusInternalServerError, utils.MakeResponse("Có lỗi xảy ra, vui lòng thử lại sau.", nil, result.Error.Error()))
		return
	}

	ctx.JSON(http.StatusOK, utils.MakeResponse("Lấy danh sách nguồn dữ liệu thành công.", gin.H{"data": records, "limit": limit, "skip": skip, "total": total}, ""))
}

func CreateChannel(ctx *gin.Context) {
	var record models.Channel
	if err := utils.GetBodyData(ctx, &record); err != nil {
		ctx.JSON(http.StatusBadRequest, utils.MakeResponse("Định dạng dữ liệu không hợp lệ.", nil, err.Error()))
		return
	}

	record.UserID = uuid.FromStringOrNil(ctx.GetString(constants.USER_ID_KEY))

	result := db.DB.Create(&record)
	if result.Error != nil {
		ctx.JSON(http.StatusInternalServerError, utils.MakeResponse("Có lỗi xảy ra, vui lòng thử lại sau.", nil, result.Error.Error()))
		return
	}
	ctx.JSON(http.StatusCreated, utils.MakeResponse("Tạo nguồn dữ liệu thành công.", record, ""))
}

func UpdateChannel(ctx *gin.Context) {
	id := ctx.Param("id")

	var record models.Channel
	if err := utils.GetBodyData(ctx, &record); err != nil {
		ctx.JSON(http.StatusBadRequest, utils.MakeResponse("Định dạng dữ liệu không hợp lệ.", nil, err.Error()))
		return
	}

	// Kiểm tra user_id trước khi update
	existingRecord := models.Channel{}
	result := db.DB.Where("id = ?", id).First(&existingRecord)
	if result.Error != nil {
		if errors.Is(result.Error, gorm.ErrRecordNotFound) {
			ctx.JSON(http.StatusNotFound, utils.MakeResponse("Không tìm thấy nguồn dữ liệu.", nil, result.Error.Error()))
			return
		}
		ctx.JSON(http.StatusInternalServerError, utils.MakeResponse("Có lỗi xảy ra, vui lòng thử lại sau.", nil, result.Error.Error()))
		return
	}

	if existingRecord.UserID != uuid.FromStringOrNil(ctx.GetString(constants.USER_ID_KEY)) {
		ctx.JSON(http.StatusForbidden, utils.MakeResponse("Bạn không có quyền truy cập tài nguyên này.", nil, ""))
		return
	}

	// Cập nhật chỉ các trường cần thiết
	db.DB.Model(&models.Channel{}).Where("id = ?", id).Select("Name", "Description", "Config").Updates(&record)

	ctx.JSON(http.StatusOK, utils.MakeResponse("Cập nhật thông tin nguồn dữ liệu thành công.", record, ""))
}

func DeleteChannel(ctx *gin.Context) {
	id := ctx.Param("id")

	// Kiểm tra user_id trước khi update
	existingRecord := models.Channel{}
	result := db.DB.Where("id = ?", id).First(&existingRecord)
	if result.Error != nil {
		if errors.Is(result.Error, gorm.ErrRecordNotFound) {
			ctx.JSON(http.StatusNotFound, utils.MakeResponse("Không tìm thấy nguồn dữ liệu.", nil, result.Error.Error()))
			return
		}
		ctx.JSON(http.StatusInternalServerError, utils.MakeResponse("Có lỗi xảy ra, vui lòng thử lại sau.", nil, result.Error.Error()))
		return
	}

	if existingRecord.UserID != uuid.FromStringOrNil(ctx.GetString(constants.USER_ID_KEY)) {
		ctx.JSON(http.StatusForbidden, utils.MakeResponse("Bạn không có quyền truy cập tài nguyên này.", nil, ""))
		return
	}

	result = db.DB.Where("id = ?", id).Delete(&models.Channel{})

	if result.RowsAffected == 0 {
		ctx.JSON(http.StatusNotFound, utils.MakeResponse("Không tìm thấy nguồn dữ liệu.", nil, ""))
		return
	} else if result.Error != nil {
		ctx.JSON(http.StatusInternalServerError, utils.MakeResponse("Có lỗi xảy ra, vui lòng thử lại sau.", nil, result.Error.Error()))
		return
	}

	ctx.JSON(http.StatusOK, utils.MakeResponse("Xóa nguồn dữ liệu thành công.", nil, ""))
}
