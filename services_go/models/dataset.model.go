package models

import (
	uuid "github.com/satori/go.uuid"
)

type Dataset struct {
	Base
	UserID     uuid.UUID `json:"user_id" gorm:"type:uuid;not null;default:null"`
	DataMartID uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4()" json:"data_mart_id"`
	Name       string    `json:"name" gorm:"not null;default:null"`
	SQLQuery   string    `json:"sql_query" gorm:"not null;default:null"`
}
