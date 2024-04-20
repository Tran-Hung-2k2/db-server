package utils

import (
	"db-server/constants"
	"errors"
	"fmt"
	"reflect"

	"github.com/gin-gonic/gin"
	"github.com/mitchellh/mapstructure"
	"gorm.io/gorm"
)

func GetBodyData(ctx *gin.Context, data interface{}) error {
	// Get the validated data from the context and perform a type assertion
	validData, exists := ctx.Get(constants.BODY_DATA_KEY)
	if !exists {
		return errors.New("not found valid data in context")
	}

	err := mapstructure.Decode(validData, &data)
	if err != nil {
		return err
	}

	return nil
}

func AddQueryData(ctx *gin.Context, query *gorm.DB) (*gorm.DB, error) {
	queryParams, exists := ctx.Get(constants.QUERY_DATA_KEY)
	if !exists {
		return nil, errors.New("not found valid data in context")
	}
	// Thêm điều kiện vào truy vấn nếu giá trị không rỗng
	values := reflect.ValueOf(queryParams).Elem()
	types := reflect.TypeOf(queryParams).Elem()

	for i := 0; i < values.NumField(); i++ {
		field := types.Field(i)
		value := values.Field(i)

		if value.Interface() != nil && value.Interface() != "" {
			query = query.Where(fmt.Sprintf("%s = ?", field.Name), value.Interface())
		}
	}

	return query, nil
}
