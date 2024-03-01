package utils

import (
	"os"
)

func GetEnv(key, defaultValue string) string {
	value, exists := os.LookupEnv(key)

	if !exists {
		// Không tồn tại biến môi trường tương ứng với key thì sử dụng giá trị mặc định
		return defaultValue
	}
	return value
}
