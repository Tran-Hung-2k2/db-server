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

	// Create a new decoder with ErrorUnused set to false
	config := &mapstructure.DecoderConfig{
		Metadata:    nil,
		Result:      &data,
		ErrorUnused: false,
	}
	decoder, err := mapstructure.NewDecoder(config)
	if err != nil {
		return err
	}

	// Use the new decoder to decode the data
	err = decoder.Decode(validData)
	if err != nil {
		return err
	}

	return nil
}

func AddQueryData(ctx *gin.Context, query *gorm.DB, customParams map[string]interface{}) (*gorm.DB, error) {
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
			if field.Name == "type" && value.Kind() == reflect.Slice {
				query = query.Where(fmt.Sprintf("%s IN (?)", field.Name), value.Interface())
			} else {
				query = query.Where(fmt.Sprintf("%s = ?", field.Name), value.Interface())
			}
		}
	}

	// Thêm các param query tùy chỉnh
	for key, value := range customParams {
		if value != nil && value != "" {
			query = query.Where(fmt.Sprintf("%s = ?", key), value)
		}
	}

	return query, nil
}
