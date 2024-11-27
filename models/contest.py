from typing import List, Optional

from beanie import Document, Link
from bson import ObjectId
from pydantic import BaseModel, ConfigDict

from models.project import Project

ProjectsList = List[Link[Project]]


class Contest(Document):
    name: str
    description: str
    alive: bool = True
    projects: ProjectsList = []

    class Settings:
        name = "contests"


class AddContest(BaseModel):
    name: str
    description: str


class UpdateContest(BaseModel):
    """Модель с опциональными полями, которые можно обновить в базе данных"""

    name: Optional[str] = None
    description: Optional[str] = None
    projects: Optional[ProjectsList] = None
    alive: Optional[bool] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )
