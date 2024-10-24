from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field

from models.user import UsersList

from . import Files, Picture, PyObjectId


class Project(BaseModel):
    id: PyObjectId = Field(alias="_id")
    name: str = Field(...)
    description: str = Field(...)
    files: Files = Field(...)
    users: UsersList = UsersList()
    picture: Picture = bytes()
    boosts: int = 0

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )


class ProjectsList(BaseModel):
    value: List[Project] = []


class AddProject(BaseModel):
    name: str = Field(...)
    description: str = Field(...)
    # Архив обязателен, но для быстрой проверки убрал
    # archive: Archive = None


class UpdateProject(BaseModel):
    """Модель с опциональными полями, которые можно обновить в базе данных"""

    name: Optional[str] = None
    description: Optional[str] = None
    Users: Optional[UsersList] = None
    archive: Optional[Files] = None
    picture: Optional[Picture] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )
