from typing import List, Optional

from beanie import Document, Link
from bson import ObjectId
from pydantic import BaseModel, ConfigDict

from models.project import Project

from . import SkipId


class Contest(Document, SkipId):
    name: str
    description: str
    alive: bool = True
    projects: List[Link[Project]] = []

    class Settings:
        name = "contests"


class UpdateContest(BaseModel):
    """Модель с опциональными полями, которые можно обновить в базе данных"""

    name: Optional[str] = None
    description: Optional[str] = None
    projects: Optional[List[Project]] = None
    alive: Optional[bool] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )
