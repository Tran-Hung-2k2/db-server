package schemas

import (
	"db-server/constants"
	"db-server/models"
)

type SignUpRequest struct {
	Name     string `json:"name" validate:"required"`
	Email    string `json:"email" validate:"required,email"`
	Password string `json:"password" validate:"required"`
}

type SignUpResponse struct {
	models.Base
	Name  string             `json:"name"`
	Email string             `json:"email"`
	Role  constants.UserRole `json:"role"`
}

type SignInRequest struct {
	Email    string `json:"email" validate:"required,email"`
	Password string `json:"password" validate:"required"`
}

type SignInResponse struct {
	models.Base
	Name  string             `json:"name"`
	Email string             `json:"email"`
	Role  constants.UserRole `json:"role"`
}
