from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field

from ..annotations import Picture, PyObjectId


class Contest(BaseModel):
    id: PyObjectId = Field(alias="_id")
    name: str = Field(...)
    users: list = Field(...)
    status: bool = True
    description: Optional[str] = None
    picture: Optional[Picture] = None

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )


class ContestsList(BaseModel):
    contests: List[Contest]


class AddContest(BaseModel):
    name: str = Field(...)


class UpdateContest(BaseModel):
    """Модель с опциональными полями, которые можно обновить в базе данных"""

    name: Optional[str] = None
    users: Optional[list] = None
    status: Optional[bool] = None
    description: Optional[str] = None
    picture: Optional[Picture] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )
