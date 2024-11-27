from typing import Annotated, List, Optional

from beanie import Document, Link
from bson import ObjectId
from pydantic import BaseModel, BeforeValidator, ConfigDict

from models.user import User

from . import SkipId

Picture = Annotated[bytes, BeforeValidator(bytes)]


class Project(Document, SkipId):
    name: str
    description: str
    users: List[Link[User]] = []
    picture: Picture = bytes()
    boosts: int = 0

    class Settings:
        name = "projects"


class UpdateProject(BaseModel):
    """Модель с опциональными полями, которые можно обновить в базе данных"""

    name: Optional[str] = None
    description: Optional[str] = None
    users: Optional[List[User]] = None
    picture: Optional[Picture] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )
