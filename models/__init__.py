"""ORM модели MongoDB"""

from typing import Annotated

from fastapi import File
from PIL import Image
from pydantic import BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]
Picture = Annotated[bytes, BeforeValidator(lambda f: Image.open(f).verify())]
Files = Annotated[bytes, File]

from .contest import AddContest, Contest, ContestsList, UpdateContest
from .project import AddProject, Project, ProjectsList, UpdateProject
from .user import AddUser, UpdateUser, User, UsersList
