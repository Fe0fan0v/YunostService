# модуль содержит модели
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
import uuid


class User(BaseModel):
    # модель экземпляра пользователя
    public_id: str = Field(default=uuid.uuid4(), unique=True)
    name: Optional[str] = Field()
    surname: Optional[str] = Field()
    email: EmailStr = Field(...)
    password: str = Field(...)
    role: str = Field(default='entrant')
    courses: Optional[list] = Field()
    validated: bool = Field(default=False)
    birthday: Optional[datetime] = Field()
    registration_date: datetime = Field(default=datetime.now())


class UserLogin(BaseModel):
    # модель запроса авторизации (при регистрации используется она же)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": 'user@gmail.com',
                "password": 'password123'
            }
        }


class Profile(BaseModel):
    # модель профиля пользователя
    id: str
    name: str = None
    surname: str = None
    email: EmailStr
    role: str
    courses: list = None
    validated: bool
    birthday: datetime = None
    registration_date: datetime

    class Config:
        schema_extra = {
            "example": {
                "id": '616e424fff0d52bb0e29ce45',
                "name": "Jhon",
                "surname": "Doe",
                "email": "jhon@gmail.com",
                "role": "entrant",
                "courses": ['VR', 'JavaScript'],
                "validated": False,
                "birthday": "2004-10-19",
                "registration_date": "2021-10-19T08:58:03.277000"
            }
        }


class Message(BaseModel):
    # модель сообщения
    message: str

    class Config:
        schema_extra = {
            "example": {
                "message": 'User validated successfully',
            }
        }


class ErrorMessage(BaseModel):
    # модель сообщения об ошибке
    error: str

    class Config:
        schema_extra = {
            "example": {
                "error": 'error message',
            }
        }


class Token(BaseModel):
    # модель токена
    token: str

    class Config:
        schema_extra = {
            "example": {
                "token": 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6Im1hcnlAbWFpbC5ydSIsImV4cGlyZXMiOiIwMi8xMS8yMDIxIDA0OjIwIn0.s-kv8W9X1qEko3Qyom0akP81hgt4DHF2Ex4p__3GBj8',
            }
        }