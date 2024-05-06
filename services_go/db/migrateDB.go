package db

import (
	"db-server/utils"
)

func MigrateDB(models ...interface{}) {
	// Thêm extension vào database để tạo uuid tự động
	DB.Exec("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\"")

	// Tạo bảng từ các model
	for _, model := range models {
		DB.AutoMigrate(model)
	}

	utils.Info.Println("👍 Migration hoàn thành")
}
