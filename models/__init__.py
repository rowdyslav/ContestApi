"""ORM модели MongoDB"""

from typing import Optional

from beanie import PydanticObjectId
from pydantic import Field
from pydantic.json_schema import SkipJsonSchema


class SkipId:
    id: SkipJsonSchema[Optional[PydanticObjectId]] = Field(
        default=None, description="MongoDB document ObjectID", exclude=True
    )


from .contest import AddContest, Contest, UpdateContest
from .project import AddProject, Project, UpdateProject
from .user import UpdateUser, User
