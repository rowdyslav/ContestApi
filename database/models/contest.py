from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field

from database.models import StudentsList

from ..annotations import Picture, PyObjectId


class Contest(BaseModel):
    id: PyObjectId = Field(alias="_id")
    name: str = Field(...)
    description: str = Field(...)
    alive: bool = True
    picture: Picture = bytes()
    students: StudentsList = StudentsList()

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )


class ContestsList(BaseModel):
    value: List[Contest] = []


class AddContest(BaseModel):
    name: str = Field(...)
    description: str = Field(...)


class UpdateContest(BaseModel):
    """Модель с опциональными полями, которые можно обновить в базе данных"""

    name: Optional[str] = None
    description: Optional[str] = None
    students: Optional[StudentsList] = None
    alive: Optional[bool] = None
    picture: Optional[Picture] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )
