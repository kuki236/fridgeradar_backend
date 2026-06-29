from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=1, max_length=255)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class UpdateUserRequest(BaseModel):
    """Payload for PATCH /api/auth/me. RF-AUT-001: only fields that the
    user is allowed to change from the Settings page are exposed here.
    Email and password have dedicated flows (verification / reset).
    """
    full_name: str | None = Field(default=None, min_length=1, max_length=255)


class LogoutRequest(BaseModel):
    """Optional body for POST /api/auth/logout.

    Sending `refresh_token` here ensures BOTH tokens are revoked server-side
    (RF-AUT-004). The access token is always taken from the Authorization
    header.
    """
    refresh_token: str | None = None


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    avatar_url: str | None = None

    class Config:
        from_attributes = True
