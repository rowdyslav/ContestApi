"""ORM модели MongoDB"""


class SkipId:
    """Класс, используемый для наследования после beanie.Document, чтобы удалить _id из JSON схем пайдентика"""

    from typing import Optional

    from beanie import PydanticObjectId
    from pydantic import Field
    from pydantic.json_schema import SkipJsonSchema

    id: SkipJsonSchema[Optional[PydanticObjectId]] = Field(
        default=None, description="MongoDB document ObjectID", exclude=True
    )


from .contest import Contest, UpdateContest
from .project import Project, UpdateProject
from .user import UpdateUser, User

__all__ = [User, Project, Contest, UpdateUser, UpdateProject, UpdateContest]
