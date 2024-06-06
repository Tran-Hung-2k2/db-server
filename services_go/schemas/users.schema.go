package schemas

import (
	"db-server/models"
)

type GetUserRequest struct {
	ID    string `form:"id" validate:"omitempty,uuid4"`
	Role  string `form:"role" validate:"omitempty,oneof=User Admin"`
	Email string `form:"email" validate:"omitempty,email"`
}

type GetUserResponse struct {
	models.Base
	Name  string `json:"name"`
	Email string `json:"email"`
	Role  string `json:"role"`
}
