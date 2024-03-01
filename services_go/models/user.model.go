package models

type User struct {
	Base
	Name     string `json:"name,omitempty" gorm:"not null;default:null"`
	Email    string `json:"email,omitempty" gorm:"unique;not null;default:null"`
	Password string `json:"password,omitempty" gorm:"not null;default:null"`
	Role     string `json:"role,omitempty" gorm:"not null;default:null"`
}
