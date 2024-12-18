from typing import Annotated, Optional

from beanie import Document, Indexed
from bson import ObjectId
from fastapi import File, UploadFile
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class User(Document):  # , SkipId):
    username: Annotated[str, Indexed(unique=True)]
    email: Annotated[EmailStr, Indexed(unique=True)]
    name: str
    surname: str
    picture: Optional[bytes]

    class Settings:
        name = "users"


class AddUser(BaseModel):
    username: str
    email: EmailStr
    name: str
    surname: str


class UpdateUser(BaseModel):
    """Модель с опциональными полями, которые можно обновить в базе данных"""

    username: Optional[str] = None
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    surname: Optional[str] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )
