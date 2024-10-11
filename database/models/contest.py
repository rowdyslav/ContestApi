from typing import List

from pydantic import BaseModel, ConfigDict, Field

from ..annotations import PyObjectId


class Contest(BaseModel):
    id: PyObjectId = Field(alias="_id")
    name: str = Field(...)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )


class ContestsList(BaseModel):
    contests: List[Contest]


class AddContest(BaseModel):
    name: str = Field(...)
