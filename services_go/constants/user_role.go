package constants

import (
	"database/sql/driver"
	"errors"
)

// UserRole đại diện cho loại vai trò người dùng.
type UserRole string

const (
	User  UserRole = "User"  // Hằng số vai trò người dùng
	Admin UserRole = "Admin" // Hằng số vai trò quản trị
)

// GetName trả về tên của kiểu enum.
func (UserRole) GetName() string {
	return "user_role"
}

// GetValues trả về một mảng các giá trị của enum.
func (UserRole) GetValues() []string {
	return []string{string(User), string(Admin)}
}

// Scan triển khai giao diện sql.Scanner cho UserRole.
// Nó chuyển đổi giá trị từ cơ sở dữ liệu sang UserRole.
func (dt *UserRole) Scan(value interface{}) error {
	if value == nil {
		*dt = UserRole("")
		return nil
	}
	if bv, err := driver.String.ConvertValue(value); err == nil {
		// if this is a string type
		if v, ok := bv.(string); ok {
			*dt = UserRole(v)
			return nil
		}
	}
	return errors.New("failed to scan UserRole")
}

// Value triển khai giao diện driver.Valuer cho UserRole.
// Nó chuyển đổi UserRole thành giá trị có thể lưu trữ trong cơ sở dữ liệu.
func (dt UserRole) Value() (driver.Value, error) {
	return string(dt), nil
}
