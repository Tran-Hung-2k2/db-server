package constants

// EnumInterface đại diện cho một enum có thể tạo kiểu enum trong cơ sở dữ liệu
type EnumInterface interface {
	GetName() string
	GetValues() []string
}
