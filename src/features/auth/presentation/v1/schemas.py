from typing import Any

from pydantic import BaseModel, EmailStr, Field


class LoginUserRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)


class RefreshTokenRequest(BaseModel):
    refresh_token: str | None = None


class TokensResponse(BaseModel):
    tokens: dict[str, Any]
