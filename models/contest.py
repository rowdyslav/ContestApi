from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field

from models.project import ProjectsIdsList

from . import Picture, PyObjectId


class Contest(BaseModel):
    id: PyObjectId = Field(alias="_id")
    name: str = Field(...)
    description: str = Field(...)
    alive: bool = True
    projects_ids: ProjectsIdsList = ProjectsIdsList()

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )


class ContestsList(BaseModel):
    value: List[Contest] = []


class ContestsIdsList(BaseModel):
    value: List[PyObjectId] = []


class AddContest(BaseModel):
    name: str = Field(...)
    description: str = Field(...)


class UpdateContest(BaseModel):
    """Модель с опциональными полями, которые можно обновить в базе данных"""

    name: Optional[str] = None
    description: Optional[str] = None
    projects_ids: Optional[ProjectsIdsList] = None
    alive: Optional[bool] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )
