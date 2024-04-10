package db

import (
	"db-server/constants"
	"fmt"
	"strings"
)

func CreateEnumFromInterface(enum constants.EnumInterface) {
	// Tạo chuỗi các giá trị enum, mỗi giá trị được bao quanh bởi dấu nháy đơn
	valueStr := "'" + strings.Join(enum.GetValues(), "', '") + "'"

	// Tạo câu lệnh SQL để tạo kiểu enum
	sql := fmt.Sprintf("DO $$ BEGIN CREATE TYPE %s AS ENUM (%s); EXCEPTION WHEN duplicate_object THEN null; END $$;", enum.GetName(), valueStr)

	// Thực thi câu lệnh SQL
	DB.Exec(sql)
}

func MigrateDB(models ...interface{}) {
	// Thêm extension vào database để tạo uuid tự động
	DB.Exec("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\"")

	CreateEnumFromInterface(constants.UserRole(""))
	CreateEnumFromInterface(constants.ChannelType(""))

	// Tạo bảng từ các model
	for _, model := range models {
		DB.AutoMigrate(model)
	}

	fmt.Println("👍 Migration hoàn thành")
}
