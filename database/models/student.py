from typing import Annotated, List, Optional

from bson import ObjectId
from pydantic import BaseModel, BeforeValidator, ConfigDict, EmailStr, Field

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]


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
        json_schema_extra={
            "example": {
                "username": "janadopoe__",
                "name": "Jane ",
                "surname": "Doe",
                "email": "jdoe@example.com",
            }
        },
    )


class StudentCollection(BaseModel):
    """
    A container holding a list of `StudentModel` instances.

    This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

    students: List[Student]


class UpdateStudentModel(BaseModel):
    """
    A set of optional updates to be made to a document in the database.
    """

    name: Optional[str] = None
    email: Optional[EmailStr] = None
    course: Optional[str] = None
    gpa: Optional[float] = None
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "name": "Jane Doe",
                "email": "jdoe@example.com",
                "course": "Experiments, Science, and Fashion in Nanophotonics",
                "gpa": 3.0,
            }
        },
    )
