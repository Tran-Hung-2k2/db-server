package db

import (
	"db-server/utils"
	"fmt"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

// ORM public cho các module
var DB *gorm.DB

// ConnectToPostgres kết nối đến cơ sở dữ liệu PostgreSQL và tự động migrate bảng
func ConnectToPostgres(models ...interface{}) {
	// Đọc các biến môi trường hoặc sử dụng giá trị mặc định
	host := utils.GetEnv("DB_HOST", "127.0.0.1")
	port := utils.GetEnv("DB_PORT", "5432")
	user := utils.GetEnv("DB_USER", "postgres")
	password := utils.GetEnv("DB_PASSWORD", "postgres")
	dbname := utils.GetEnv("DB_NAME", "postgres")

	// Tạo chuỗi kết nối DSN từ biến môi trường hoặc giá trị mặc định
	dsn := fmt.Sprintf("host=%s user=%s password=%s dbname=%s port=%s sslmode=disable TimeZone=Asia/Shanghai", host, user, password, dbname, port)

	// Kết nối tới cơ sở dữ liệu
	db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{})
	if err != nil {
		utils.Warning.Println("Kết nối database thất bại")
		return
	}
	utils.Info.Println("🚀 Kết nối database thành công")

	DB = db

	// Migrate các bảng trong database
	MigrateDB(models...)
}
