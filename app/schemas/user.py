#schemas/user.py
from pydantic import BaseModel, EmailStr

# For reading user data
class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: str | None
    is_active: bool
    is_verified: bool

    class Config:
        orm_mode = True

# For user registration
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None
