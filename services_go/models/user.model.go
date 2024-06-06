package models

import (
	"golang.org/x/crypto/bcrypt"
)

type User struct {
	Base
	Name     string `json:"name" gorm:"not null;default:null"`
	Email    string `json:"email" gorm:"unique;not null;default:null"`
	Password string `json:"password" gorm:"not null;default:null"`
	Role     string `json:"role" gorm:"not null;default:null"`
}

func (u *User) HashPassword() error {
	bytes, err := bcrypt.GenerateFromPassword([]byte(u.Password), 10)
	if err != nil {
		return err
	}
	u.Password = string(bytes)
	return nil
}

func (u *User) CheckPasswordHash(password string) error {
	err := bcrypt.CompareHashAndPassword([]byte(u.Password), []byte(password))
	if err != nil {
		return err
	}
	return nil
}
