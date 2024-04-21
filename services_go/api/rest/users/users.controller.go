package users

import (
	"db-server/db"
	"db-server/models"
	"db-server/schemas"
	"db-server/utils"
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	"github.com/jinzhu/copier"
)

func GetUser(ctx *gin.Context) {
	// Khởi tạo truy vấn
	query, _ := utils.AddQueryData(ctx, db.DB)

	// Get limit and skip from query parameters
	limit, _ := strconv.Atoi(ctx.DefaultQuery("limit", "10"))
	skip, _ := strconv.Atoi(ctx.DefaultQuery("skip", "0"))

	// Get total count
	var total int64
	query.Model(&models.User{}).Count(&total)

	// Thực hiện truy vấn để lấy danh sách người dùng
	var users []models.User
	result := query.Limit(limit).Offset(skip).Find(&users)

	if result.Error != nil {
		ctx.JSON(http.StatusInternalServerError, utils.MakeResponse("Có lỗi xảy ra, vui lòng thử lại sau.", nil, result.Error.Error()))
		return
	}

	var resData []schemas.GetUserResponse
	copier.Copy(&resData, &users)

	ctx.JSON(http.StatusOK, utils.MakeResponse("Lấy danh sách người dùng thành công.", gin.H{"data": resData, "limit": limit, "skip": skip, "total": total}, ""))
}

func DeleteUser(ctx *gin.Context) {
	id := ctx.Param("id")

	result := db.DB.Where("id = ?", id).Delete(&models.User{})

	if result.RowsAffected == 0 {
		ctx.JSON(http.StatusNotFound, utils.MakeResponse("Không tìm thấy người dùng.", nil, ""))
		return
	} else if result.Error != nil {
		ctx.JSON(http.StatusInternalServerError, utils.MakeResponse("Có lỗi xảy ra, vui lòng thử lại sau.", nil, result.Error.Error()))
		return
	}

	ctx.JSON(http.StatusOK, utils.MakeResponse("Xóa người dùng thành công.", nil, ""))
}
