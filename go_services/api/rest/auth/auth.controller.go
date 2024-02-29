package auth

import (
	"db-server/db"
	"db-server/models"
	"db-server/utils"
	"net/http"

	"github.com/gin-gonic/gin"
)

func SignUp(ctx *gin.Context) {
	var user models.User

	if err := ctx.ShouldBindJSON(&user); err != nil {
		ctx.JSON(http.StatusBadRequest, gin.H{"message": "Thông tin đăng ký không hợp lệ."})
		return
	}

	user.Role = "user"

	result := db.DB.Create(&user)
	if result.Error != nil {
		ctx.JSON(http.StatusInternalServerError, gin.H{"message": "Có lỗi xảy ra, vui lòng thử lại sau."})
		return
	}

	ctx.JSON(http.StatusCreated, gin.H{"message": "Đăng ký tài khoản thành công."})
}

func SignIn(ctx *gin.Context) {
	var user models.User
	var data models.User

	if err := ctx.ShouldBindJSON(&data); err != nil {
		ctx.JSON(http.StatusBadRequest, gin.H{"message": "Thông tin đăng nhập không hợp lệ."})
		return
	}

	result := db.DB.First(&user, "email = ?", data.Email)
	if result.Error != nil {
		ctx.JSON(http.StatusInternalServerError, gin.H{"message": "Có lỗi xảy ra, vui lòng thử lại sau."})
		return
	}

	if data.Password == user.Password {
		token, _ := utils.CreateAccessToken(map[string]interface{}{
			"id":   user.ID,
			"role": user.Role,
		})

		// Đặt access token vào cookie
		ctx.SetCookie("access_token", token, 0, "/", "", false, true)

		ctx.JSON(http.StatusOK, gin.H{"message": "Đăng nhập thành công."})
	} else {
		ctx.JSON(http.StatusBadRequest, gin.H{"message": "Tài khoản hoặc mật khẩu không chính xác."})
	}
}

func Logout(ctx *gin.Context) {
	// Xóa cookie access_token
	ctx.SetCookie("access_token", "", -1, "/", "", false, true)

	ctx.JSON(http.StatusOK, gin.H{"message": "Đăng xuất thành công."})
}
