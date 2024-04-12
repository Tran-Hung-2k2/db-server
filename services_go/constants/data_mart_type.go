package constants

import (
	"database/sql/driver"
	"errors"
)

// DataMartType đại diện cho loại vai trò người dùng.
type DataMartType string

const (
	Dataset  DataMartType = "Dataset"
	DataMart DataMartType = "DataMart"
)

// GetName trả về tên của kiểu enum.
func (DataMartType) GetName() string {
	return "data_mart_type"
}

// GetValues trả về một mảng các giá trị của enum.
func (DataMartType) GetValues() []string {
	return []string{string(Dataset), string(DataMart)}
}

// Scan triển khai giao diện sql.Scanner cho DataMartType.
// Nó chuyển đổi giá trị từ cơ sở dữ liệu sang DataMartType.
func (dt *DataMartType) Scan(value interface{}) error {
	if value == nil {
		*dt = DataMartType("")
		return nil
	}
	if bv, err := driver.String.ConvertValue(value); err == nil {
		// if this is a string type
		if v, ok := bv.(string); ok {
			*dt = DataMartType(v)
			return nil
		}
	}
	return errors.New("failed to scan DataMartType")
}

// Value triển khai giao diện driver.Valuer cho DataMartType.
// Nó chuyển đổi DataMartType thành giá trị có thể lưu trữ trong cơ sở dữ liệu.
func (dt DataMartType) Value() (driver.Value, error) {
	return string(dt), nil
}
