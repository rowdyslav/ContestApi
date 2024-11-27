from typing import Annotated, Optional

from beanie import Document, Indexed, PydanticObjectId
from bson import ObjectId
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from pydantic.json_schema import SkipJsonSchema

from . import SkipId


class User(Document, SkipId):
    # id: SkipJsonSchema[Optional[PydanticObjectId]] = Field(
    #     default=None, description="MongoDB document ObjectID", exclude=True
    # )
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
