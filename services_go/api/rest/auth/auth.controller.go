package auth

import (
	"db-server/constants"
	"db-server/db"
	"db-server/models"
	"db-server/schemas"
	"db-server/utils"
	"errors"
	"net/http"
	"strings"

	"github.com/gin-gonic/gin"
	"github.com/jinzhu/copier"
	"gorm.io/gorm"
)

// Hàm SignUp xử lý việc đăng ký tài khoản
func SignUp(ctx *gin.Context) {
	var data_schema schemas.SignUpRequest
	utils.GetBodyData(ctx, &data_schema)
	if data_schema.Confirm_Password != data_schema.Password {
		ctx.JSON(http.StatusBadRequest, utils.MakeResponse("Mật khẩu xác nhận không chính xác.", nil, ""))
		return
	}

	// Get the validated data from the context and perform a type assertion
	var data models.User
	if err := utils.GetBodyData(ctx, &data); err != nil {
		ctx.JSON(http.StatusBadRequest, utils.MakeResponse("Định dạng dữ liệu không hợp lệ.", nil, err.Error()))
		return
	}

	data.Role = constants.User

	// Mã hóa mật khẩu của người dùng
	data.HashPassword()

	// Lưu user vào cơ sở dữ liệu
	result := db.DB.Create(&data)

	if result.Error != nil {
		// Kiểm tra lỗi do vi phạm ràng buộc duy nhất của trường email
		if strings.Contains(result.Error.Error(), "uni_users_email") {
			ctx.JSON(http.StatusBadRequest, utils.MakeResponse("Email đã được đăng ký tài khoản trước đó.", nil, ""))
		} else {
			ctx.JSON(http.StatusInternalServerError, utils.MakeResponse("Có lỗi xảy ra, vui lòng thử lại sau.", nil, result.Error.Error()))
		}
		return
	}

	// Tạo SignUpResponse từ user
	var resData schemas.SignUpResponse
	copier.Copy(&resData, &data)

	ctx.JSON(http.StatusCreated, utils.MakeResponse("Đăng ký tài khoản thành công.", resData, ""))
}

// Hàm SignIn xử lý việc đăng nhập
func SignIn(ctx *gin.Context) {
	// Get the validated data from the context and perform a type assertion
	var data models.User
	if err := utils.GetBodyData(ctx, &data); err != nil {
		ctx.JSON(http.StatusBadRequest, utils.MakeResponse("Định dạng dữ liệu không hợp lệ.", nil, err.Error()))
		return
	}

	var user models.User
	// Tìm kiếm user trong cơ sở dữ liệu dựa trên email
	result := db.DB.First(&user, "email = ?", data.Email)
	if result.Error != nil {
		if errors.Is(result.Error, gorm.ErrRecordNotFound) {
			ctx.JSON(http.StatusBadRequest, utils.MakeResponse("Tài khoản hoặc mật khẩu không chính xác.", nil, ""))
		} else {
			ctx.JSON(http.StatusInternalServerError, utils.MakeResponse("Có lỗi xảy ra, vui lòng thử lại sau.", nil, result.Error.Error()))
		}
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
		ctx.SetSameSite(http.SameSiteNoneMode)
		ctx.SetCookie(constants.ACCESS_TOKEN_KEY, token, 3*24*60*60, "/", "", true, true)

		var resData schemas.SignInResponse
		copier.Copy(&resData, &user)

		ctx.JSON(http.StatusOK, utils.MakeResponse("Đăng nhập thành công.", resData, ""))
	} else {
		ctx.JSON(http.StatusBadRequest, utils.MakeResponse("Tài khoản hoặc mật khẩu không chính xác.", nil, ""))
	}
}

// Hàm Logout xử lý việc đăng xuất
func Logout(ctx *gin.Context) {
	// Xóa cookie access_token
	ctx.SetCookie(constants.ACCESS_TOKEN_KEY, "", -1, "/", "", false, true)

	ctx.JSON(http.StatusOK, utils.MakeResponse("Đăng xuất thành công.", nil, ""))
}
