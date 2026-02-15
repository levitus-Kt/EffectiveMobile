from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# Схема для регистрации
class UserCreate(BaseModel):
    first_name: str = Field(..., min_length=2)
    last_name: str = Field(..., min_length=2)
    middle_name: Optional[str] = None
    email: EmailStr
    password: str = Field(..., min_length=5)
    password_repeat: str

# Схема для авторизации
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Схема профиля пользователя
class UserProfile(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    role_id: int
    is_active: bool