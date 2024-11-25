from typing import Annotated, List, Optional

from beanie import Document, Indexed, PydanticObjectId
from bson import ObjectId
from pydantic import BaseModel, ConfigDict, EmailStr


class User(Document):
    username: Annotated[str, Indexed(unique=True)]
    name: str
    surname: str
    email: Annotated[EmailStr, Indexed(unique=True)]

    class Settings:
        name = "users"


class AddUser(BaseModel):
    username: str
    name: str
    surname: str
    email: EmailStr


class UpdateUser(BaseModel):
    """Модель с опциональными полями, которые можно обновить в базе данных"""

    username: Optional[str] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[EmailStr] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )
