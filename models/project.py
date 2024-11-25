from typing import Annotated, List, Optional

from beanie import Document, Link
from bson import ObjectId
from pydantic import BaseModel, BeforeValidator, ConfigDict

from models.user import User

Picture = Annotated[bytes, BeforeValidator(bytes)]
UsersList = List[Link[User]]


class Project(Document):
    name: str
    description: str
    users: UsersList = []
    picture: Picture = bytes()
    boosts: int = 0

    class Settings:
        name = "projects"


class AddProject(BaseModel):
    name: str
    description: str
    # Архив обязателен, но для быстрой проверки убрал
    # archive: Archive = None


class UpdateProject(BaseModel):
    """Модель с опциональными полями, которые можно обновить в базе данных"""

    name: Optional[str] = None
    description: Optional[str] = None
    users: Optional[UsersList] = None
    picture: Optional[Picture] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )
