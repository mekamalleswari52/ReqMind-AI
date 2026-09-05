from pydantic import BaseModel, EmailStr, ConfigDict


class UserOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)
