from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from ..annotations import PyObjectId


class Student(BaseModel):
    """Контейнер для одной записи студента."""

    # Первичный ключ для StudentModel, хранящийся в экземпляре как `str`.
    # Это будет иметь псевдоним `_id` при отправке в MongoDB,
    # но указывается как `id` в запросах и ответах API.
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    username: str = Field(...)
    name: str = Field(...)
    surname: str = Field(...)
    email: EmailStr = Field(...)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )


class StudentCollection(BaseModel):
    """
    A container holding a list of `StudentModel` instances.

    This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

    students: List[Student]


class UpdateStudent(BaseModel):
    """
    A set of optional updates to be made to a document in the database.
    """

    username: Optional[str] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[EmailStr] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )
