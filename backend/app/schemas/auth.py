from pydantic import BaseModel, EmailStr, ConfigDict


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    confirm_password: str

    model_config = ConfigDict(str_strip_whitespace=True)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
