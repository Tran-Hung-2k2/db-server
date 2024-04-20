package validations

import (
	"db-server/constants"
	"db-server/utils"
	"net/http"
	"strings"

	"github.com/gin-gonic/gin"
	"github.com/go-playground/locales/vi"
	ut "github.com/go-playground/universal-translator"
	"github.com/go-playground/validator/v10"
	vi_translations "github.com/go-playground/validator/v10/translations/vi"
)

func BodyValidation(ctx *gin.Context, data interface{}, errorMessages map[string]string) error {
	resMessage := ""

	// Kiểm tra và bind dữ liệu từ request body vào biến data
	if err := ctx.ShouldBindJSON(data); err != nil {
		utils.Error.Println(err.Error())

		for tag, message := range errorMessages {
			if strings.Contains(err.Error(), tag) {
				resMessage = message
			} else {
				resMessage = "Định dạng dữ liệu không hợp lệ."
			}
		}

		ctx.JSON(http.StatusBadRequest, utils.MakeResponse(resMessage, nil, err.Error()))
		return err
	}

	if err := BaseValidation(ctx, data, errorMessages); err != nil {
		return err
	}

	// Store the validated data in the context
	ctx.Set(constants.BODY_DATA_KEY, data)

	return nil
}

func QueryValidation(ctx *gin.Context, data interface{}, errorMessages map[string]string) error {
	resMessage := ""

	// Kiểm tra và bind dữ liệu từ request query vào biến data
	if err := ctx.ShouldBindQuery(data); err != nil {
		utils.Error.Println(err.Error())

		for tag, message := range errorMessages {
			if strings.Contains(err.Error(), tag) {
				resMessage = message
			} else {
				resMessage = "Định dạng dữ liệu không hợp lệ."
			}
		}

		ctx.JSON(http.StatusBadRequest, utils.MakeResponse(resMessage, nil, err.Error()))
		return err
	}

	if err := BaseValidation(ctx, data, errorMessages); err != nil {
		return err
	}

	// Store the validated data in the context
	ctx.Set(constants.QUERY_DATA_KEY, data)

	return nil
}

func BaseValidation(ctx *gin.Context, data interface{}, errorMessages map[string]string) error {
	resMessage := ""

	// Create a new validator instance
	validate := validator.New()

	// Validate the data
	err := validate.Struct(data)
	if err != nil {
		// Validation failed, handle the error
		errors := err.(validator.ValidationErrors)

		// Create a translator
		vi := vi.New()
		uni := ut.New(vi, vi)
		trans, _ := uni.GetTranslator("vi")

		// Register translations
		_ = vi_translations.RegisterDefaultTranslations(validate, trans)

		// Iterate over the errors and add the translated error messages
		var translatedErrors []string
		for _, e := range errors {
			translatedErrors = append(translatedErrors, e.Translate(trans))
		}

		utils.Error.Println(errors.Error())

		// Check if the error message contains any of the specified tags
		for tag, message := range errorMessages {
			if strings.Contains(errors.Error(), tag) {
				resMessage = message
			} else if strings.Contains(errors.Error(), "'required' tag") {
				resMessage = translatedErrors[0]
			} else if strings.Contains(errors.Error(), "'uuid4' tag") {
				resMessage = translatedErrors[0]
			} else {
				resMessage = "Định dạng dữ liệu không hợp lệ."
			}
		}

		ctx.JSON(http.StatusBadRequest, utils.MakeResponse(resMessage, nil, strings.Join(translatedErrors, "; ")))
		return errors
	}

	return nil
}
