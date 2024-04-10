package auth

import (
	"db-server/constants"
	"db-server/db"
	"db-server/models"
	"db-server/utils"
	"net/http"

	"github.com/gin-gonic/gin"
)

// Hàm SignUp xử lý việc đăng ký tài khoản
func SignUp(ctx *gin.Context) {
	var user models.User

	// Kiểm tra và bind dữ liệu từ request body vào biến user
	if err := ctx.ShouldBindJSON(&user); err != nil {
		ctx.JSON(http.StatusBadRequest, gin.H{"message": "Thông tin đăng ký không hợp lệ."})
		return
	}

	user.Role = constants.User

	// Mã hóa mật khẩu của user
	user.HashPassword()

	// Lưu user vào cơ sở dữ liệu
	result := db.DB.Create(&user)
	if result.Error != nil {
		ctx.JSON(http.StatusInternalServerError, gin.H{"message": "Có lỗi xảy ra, vui lòng thử lại sau."})
		return
	}

	ctx.JSON(http.StatusCreated, gin.H{"message": "Đăng ký tài khoản thành công."})
}

// Hàm SignIn xử lý việc đăng nhập
func SignIn(ctx *gin.Context) {
	var user models.User
	var data models.User

	// Kiểm tra và bind dữ liệu từ request body vào biến data
	if err := ctx.ShouldBindJSON(&data); err != nil {
		ctx.JSON(http.StatusBadRequest, gin.H{"message": "Thông tin đăng nhập không hợp lệ."})
		return
	}

	// Tìm kiếm user trong cơ sở dữ liệu dựa trên email
	result := db.DB.First(&user, "email = ?", data.Email)
	if result.Error != nil {
		ctx.JSON(http.StatusInternalServerError, gin.H{"message": "Có lỗi xảy ra, vui lòng thử lại sau."})
		return
	}

	// Kiểm tra mật khẩu
	if user.CheckPasswordHash(data.Password) == nil {
		// Tạo access token
		token, _ := utils.CreateAccessToken(map[string]interface{}{
			"id":   user.ID,
			"role": user.Role,
		})

		// Đặt access token vào cookie
		ctx.SetCookie("access_token", token, 0, "/", "", false, true)

		ctx.JSON(http.StatusOK, gin.H{"message": "Đăng nhập thành công.", "data": user})
	} else {
		ctx.JSON(http.StatusBadRequest, gin.H{"message": "Tài khoản hoặc mật khẩu không chính xác."})
	}
}

// Hàm Logout xử lý việc đăng xuất
func Logout(ctx *gin.Context) {
	// Xóa cookie access_token
	ctx.SetCookie("access_token", "", -1, "/", "", false, true)

	ctx.JSON(http.StatusOK, gin.H{"message": "Đăng xuất thành công."})
}
