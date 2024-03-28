package utils

import (
	"time"

	"github.com/golang-jwt/jwt/v5"
)

func CreateAccessToken(data map[string]interface{}) (string, error) {
	secretKey := []byte(GetEnv("JWT_ACCESS_KEY", "secretKey"))
	expTime := time.Now().Add(2000000 * 60 * 60 * time.Second).Unix() // 60 minute
	return CreateToken(data, secretKey, expTime)
}

func VerifyAccessToken(tokenString string, dataKeys []string) (map[string]string, error) {
	secretKey := []byte(GetEnv("JWT_ACCESS_KEY", "secretKey"))
	return VerifyToken(tokenString, secretKey, dataKeys)
}

/*
-----------------------------------------------------------------------------------------
*/
func CreateToken(data map[string]interface{}, secretKey []byte, exp int64) (string, error) {
	// Tạo map claims
	claims := jwt.MapClaims{}

	// Thêm exp vào claims
	claims["exp"] = exp

	// Thêm các key-value từ data vào claims
	for key, value := range data {
		claims[key] = value
	}

	// Tạo token với claims
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)

	// Ký và nhận chuỗi token
	tokenString, err := token.SignedString(secretKey)
	if err != nil {
		return "", err
	}

	return tokenString, nil
}

func VerifyToken(tokenString string, secretKey []byte, dataKeys []string) (map[string]string, error) {
	token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
		return secretKey, nil
	})

	if err != nil {
		return nil, err
	}

	claims, _ := token.Claims.(jwt.MapClaims)

	data := make(map[string]string)
	for _, key := range dataKeys {
		if value, exists := claims[key]; exists {
			data[key] = value.(string)
		}
	}

	return data, err
}
