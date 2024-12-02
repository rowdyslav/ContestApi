from typing import Annotated, List, Optional

from beanie import Document, Indexed, Link
from bson import ObjectId
from models.project import Project
from pydantic import BaseModel, ConfigDict

from . import SkipId


class Contest(Document, SkipId):
    title: Annotated[str, Indexed(unique=True)]
    description: str
    alive: bool = True
    projects: List[Link[Project]] = []

    class Settings:
        name = "contests"


class UpdateContest(BaseModel):
    """Модель с опциональными полями, которые можно обновить в базе данных"""

    title: Optional[str] = None
    description: Optional[str] = None
    projects: Optional[List[Project]] = None
    alive: Optional[bool] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )
