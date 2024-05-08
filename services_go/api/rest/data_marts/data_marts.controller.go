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

func GetDataMart(ctx *gin.Context) {
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

	if !utils.Contains(sort_by, []string{"id", "created_at", "updated_at", "user_id", "name"}) {
		sort_by = "created_at"
	}
	if !utils.Contains(sort_dim, []string{"asc", "desc"}) {
		sort_dim = "desc"
	}

	// Get total count
	var total int64
	query.Model(&models.DataMart{}).Where("LOWER(name) LIKE LOWER(?)", "%"+name+"%").Count(&total)

	var records []models.DataMart
	result := query.Where("LOWER(name) LIKE LOWER(?)", "%"+name+"%").Order(fmt.Sprintf("%s %s", sort_by, sort_dim)).Limit(limit).Offset(skip).Find(&records)

	if result.Error != nil {
		ctx.JSON(http.StatusInternalServerError, utils.MakeResponse("Có lỗi xảy ra, vui lòng thử lại sau.", nil, result.Error.Error()))
		return
	}

	ctx.JSON(http.StatusOK, utils.MakeResponse("Lấy danh sách kho dữ liệu thành công.", gin.H{"data": records, "limit": limit, "skip": skip, "total": total}, ""))
}

func CreateDataMart(ctx *gin.Context) {
	var record models.DataMart
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

	ctx.JSON(http.StatusCreated, utils.MakeResponse("Tạo kho dữ liệu thành công.", record, ""))
}

func UpdateDataMart(ctx *gin.Context) {
	id := ctx.Param("id")

	var record models.DataMart
	if err := utils.GetBodyData(ctx, &record); err != nil {
		ctx.JSON(http.StatusBadRequest, utils.MakeResponse("Định dạng dữ liệu không hợp lệ.", nil, err.Error()))
		return
	}

	// Kiểm tra user_id trước khi update
	existingRecord := models.DataMart{}
	result := db.DB.Where("id = ?", id).First(&existingRecord)
	if result.Error != nil {
		if errors.Is(result.Error, gorm.ErrRecordNotFound) {
			ctx.JSON(http.StatusNotFound, utils.MakeResponse("Không tìm thấy kho dữ liệu.", nil, result.Error.Error()))
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
	db.DB.Model(&models.DataMart{}).Where("id = ?", id).Select("Name", "Description", "Schema").Updates(&record)

	ctx.JSON(http.StatusOK, utils.MakeResponse("Cập nhật thông tin kho dữ liệu thành công.", record, ""))
}

func DeleteDataMart(ctx *gin.Context) {
	id := ctx.Param("id")

	// Kiểm tra user_id trước khi update
	existingRecord := models.DataMart{}
	result := db.DB.Where("id = ?", id).First(&existingRecord)
	if result.Error != nil {
		if errors.Is(result.Error, gorm.ErrRecordNotFound) {
			ctx.JSON(http.StatusNotFound, utils.MakeResponse("Không tìm thấy kho dữ liệu.", nil, result.Error.Error()))
			return
		}
		ctx.JSON(http.StatusInternalServerError, utils.MakeResponse("Có lỗi xảy ra, vui lòng thử lại sau.", nil, result.Error.Error()))
		return
	}

	if existingRecord.UserID != uuid.FromStringOrNil(ctx.GetString(constants.USER_ID_KEY)) {
		ctx.JSON(http.StatusForbidden, utils.MakeResponse("Bạn không có quyền truy cập tài nguyên này.", nil, ""))
		return
	}

	result = db.DB.Where("id = ?", id).Delete(&models.DataMart{})

	if result.RowsAffected == 0 {
		ctx.JSON(http.StatusNotFound, utils.MakeResponse("Không tìm thấy kho dữ liệu.", nil, ""))
		return
	} else if result.Error != nil {
		ctx.JSON(http.StatusInternalServerError, utils.MakeResponse("Có lỗi xảy ra, vui lòng thử lại sau.", nil, result.Error.Error()))
		return
	}

	ctx.JSON(http.StatusOK, utils.MakeResponse("Xóa kho dữ liệu thành công.", nil, ""))
}
