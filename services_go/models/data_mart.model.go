package models

import (
	uuid "github.com/satori/go.uuid"
	"gorm.io/datatypes"
)

type DataMart struct {
	Base
	UserID      uuid.UUID      `json:"user_id" gorm:"type:uuid;not null;default:null"`
	Name        string         `json:"name" gorm:"not null;default:null"`
	Description string         `json:"description" gorm:"default:null"`
	Schema      datatypes.JSON `json:"schema" gorm:"default:null"`
}
