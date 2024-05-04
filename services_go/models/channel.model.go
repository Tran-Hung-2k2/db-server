package models

import (
	"db-server/constants"

	uuid "github.com/satori/go.uuid"
	"gorm.io/datatypes"
)

type Channel struct {
	Base
	UserID      uuid.UUID             `json:"user_id" gorm:"type:uuid;not null;default:null"`
	Name        string                `json:"name" gorm:"not null;default:null"`
	Type        constants.ChannelType `json:"type" gorm:"type:channel_type;not null;default:null;"`
	Description string                `json:"description" gorm:"default:null"`
	Config      datatypes.JSON        `json:"config" gorm:"default:null"`
}
