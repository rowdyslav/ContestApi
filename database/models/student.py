from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from ..annotations import PyObjectId


class Student(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    username: str = Field(...)
    name: str = Field(...)
    surname: str = Field(...)
    email: EmailStr = Field(...)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )


class StudentCollection(BaseModel):
    students: List[Student]


class AddStudent(BaseModel):
    username: str = Field(...)
    name: str = Field(...)
    surname: str = Field(...)
    email: EmailStr = Field(...)


class UpdateStudent(BaseModel):
    """Модель с опциональными полями, которые можно обновить в базе данных"""

    username: Optional[str] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[EmailStr] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )
