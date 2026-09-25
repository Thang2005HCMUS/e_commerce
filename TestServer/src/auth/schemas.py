from pydantic import BaseModel, EmailStr, Field

class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=4, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)

class LoginRequest(BaseModel):
    username: str = Field(...)
    password: str = Field(...)

class AuthResponse(BaseModel):
    accessToken: str
    tokenType: str = "Bearer"