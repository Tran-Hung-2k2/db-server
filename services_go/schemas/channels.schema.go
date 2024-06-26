package schemas

import "encoding/json"

type GetChannelRequest struct {
	ID      string `form:"id" validate:"omitempty,uuid4"`
	User_ID string `form:"user_id" validate:"omitempty,uuid4"`
	Type    string `form:"type" validate:"omitempty,oneof=API MySQL PostgreSQL MongoDB MinIO Snowflake 'Amazon S3' 'Oracle DB' 'Azure Blob Storage' 'Google Big Query' 'Upload File'"`
}

type GetChannelDistinctValues struct {
	Field string `form:"field" validate:"omitempty,oneof=type name"`
}

type CreateChannelRequest struct {
	Name        string          `form:"name" validate:"required"`
	Type        string          `form:"type" validate:"required"`
	Description string          `form:"description"`
	Config      json.RawMessage `form:"config" validate:"omitempty"`
}

type UpdateChannelRequest struct {
	Name        string          `form:"name" validate:"omitempty"`
	Description string          `form:"description" validate:"omitempty"`
	Config      json.RawMessage `form:"config" validate:"omitempty"`
}
