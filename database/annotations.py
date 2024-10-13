from typing import Annotated
from pydantic import BeforeValidator
from fastapi import File

PyObjectId = Annotated[str, BeforeValidator(str)]
Picture = Annotated[bytes, File()]
