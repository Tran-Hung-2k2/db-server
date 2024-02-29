package models

import (
	uuid "github.com/satori/go.uuid"
	"gorm.io/datatypes"
)

type Datasource struct {
	Base
	UserID uuid.UUID      `gorm:"type:uuid;not null;default:null" json:"user_id"`
	Name   string         `json:"name,omitempty" gorm:"not null;default:null"`
	Type   string         `json:"type,omitempty" gorm:"unique;not null;default:null"`
	Host   string         `json:"host,omitempty" gorm:"not null;default:null"`
	Port   string         `json:"port,omitempty" gorm:"not null;default:null"`
	Other  datatypes.JSON `json:"other,omitempty"`
}
