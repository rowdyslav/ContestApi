from typing import Annotated, List, Optional

from beanie import Document, Indexed, Link
from bson import ObjectId
from models.user import User
from pydantic import BaseModel, ConfigDict

from . import SkipId


class Project(Document):  # , SkipId):
    title: Annotated[str, Indexed(unique=True)]
    description: str
    users: List[Link[User]] = []
    boosts: int = 0

    class Settings:
        name = "projects"


class UpdateProject(BaseModel):
    """Модель с опциональными полями, которые можно обновить в базе данных"""

    title: Optional[str] = None
    description: Optional[str] = None
    users: Optional[List[User]] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )
