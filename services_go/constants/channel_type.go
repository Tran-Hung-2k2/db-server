package constants

import (
	"database/sql/driver"
	"errors"
)

// ChannelType đại diện cho loại Channel.
type ChannelType string

const (
	API              ChannelType = "API"
	MySQL            ChannelType = "MySQL"
	PostgreSQL       ChannelType = "PostgreSQL"
	MongoDB          ChannelType = "MongoDB"
	MinIO            ChannelType = "MinIO"
	Snowflake        ChannelType = "Snowflake"
	AmazonS3         ChannelType = "Amazon S3"
	OracleDB         ChannelType = "Oracle DB"
	AzureBlobStorage ChannelType = "Azure Blob Storage"
	GoogleBigQuery   ChannelType = "Google Big Query"
	UploadFile       ChannelType = "Upload File"
)

// GetName trả về tên của kiểu enum.
func (ChannelType) GetName() string {
	return "channel_type"
}

// GetValues trả về một mảng các giá trị của enum.
func (ChannelType) GetValues() []string {
	return []string{
		string(API),
		string(MySQL),
		string(PostgreSQL),
		string(MongoDB),
		string(MinIO),
		string(Snowflake),
		string(AmazonS3),
		string(OracleDB),
		string(AzureBlobStorage),
		string(GoogleBigQuery),
		string(UploadFile),
	}
}

// Scan triển khai giao diện sql.Scanner cho ChannelType.
// Nó chuyển đổi giá trị từ cơ sở dữ liệu sang ChannelType.
func (dt *ChannelType) Scan(value interface{}) error {
	if value == nil {
		*dt = ChannelType("")
		return nil
	}
	if bv, err := driver.String.ConvertValue(value); err == nil {
		// if this is a string type
		if v, ok := bv.(string); ok {
			*dt = ChannelType(v)
			return nil
		}
	}
	return errors.New("failed to scan ChannelType")
}

// Value triển khai giao diện driver.Valuer cho ChannelType.
// Nó chuyển đổi ChannelType thành giá trị có thể lưu trữ trong cơ sở dữ liệu.
func (dt ChannelType) Value() (driver.Value, error) {
	return string(dt), nil
}
