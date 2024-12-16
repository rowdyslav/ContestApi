from typing import Annotated, Optional

from beanie import Document, Indexed
from bson import ObjectId
from pydantic import BaseModel, ConfigDict, EmailStr


class User(Document):  # , SkipId):
    username: Annotated[str, Indexed(unique=True)]
    email: Annotated[EmailStr, Indexed(unique=True)]
    name: str
    surname: str

    class Settings:
        name = "users"


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
