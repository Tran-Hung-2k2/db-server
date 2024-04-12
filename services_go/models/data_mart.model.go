package models

import (
	"db-server/constants"

	uuid "github.com/satori/go.uuid"
	"gorm.io/datatypes"
)

type DataMart struct {
	Base
	UserID uuid.UUID              `json:"user_id" gorm:"type:uuid;not null;default:null"`
	Name   string                 `json:"name" gorm:"not null;default:null"`
	Type   constants.DataMartType `json:"type" gorm:"type:data_mart_type;not null;default:null"`
	Schema datatypes.JSON         `json:"schema" gorm:"default:null"`
}
