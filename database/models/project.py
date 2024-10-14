from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field
from database.models.student import StudentsList

from ..annotations import Archive, PyObjectId, Picture


class Project(BaseModel):
    id: PyObjectId = Field(alias="_id")
    name: str = Field(...)
    description: str = Field(...)
    archive: Archive = None     # Архив обязателен, но для быстрой проверки поставил None
    students: StudentsList = StudentsList()
    picture: Optional[Picture] = None

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )


class ProjectsList(BaseModel):
    projects: List[Project] = []


class AddProject(BaseModel):
    name: str = Field(...)
    description: str = Field(...)
    #Архив обязателен, но для быстрой проверки убрал
    #archive: Archive = None


class UpdateProject(BaseModel):
    """Модель с опциональными полями, которые можно обновить в базе данных"""

    name: Optional[str] = None
    description: Optional[str] = None
    students: Optional[StudentsList] = None
    archive: Optional[Archive] = None
    picture: Optional[Picture] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )