package schemas

import "encoding/json"

type GetDataMartRequest struct {
	ID      string `form:"id" validate:"omitempty,uuid4"`
	User_ID string `form:"user_id" validate:"omitempty,uuid4"`
}

type CreateDataMartRequest struct {
	Name        string          `form:"name" validate:"required"`
	Description string          `form:"description" validate:"omitempty"`
	Schema      json.RawMessage `form:"schema" validate:"required"`
}

type UpdateDataMartRequest struct {
	Name        string          `form:"name" validate:"omitempty"`
	Description string          `form:"description" validate:"omitempty"`
	Schema      json.RawMessage `form:"schema" validate:"omitempty"`
}
