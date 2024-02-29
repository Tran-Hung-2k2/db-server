package db

import (
	"fmt"
)

func MigrateDB(model interface{}) {
	// Thêm extension vào database để tạo uuid tự động
	DB.Exec("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\"")
	DB.AutoMigrate(model)
	fmt.Println("👍 Migration hoàn thành")
}
