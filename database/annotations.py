from typing import Annotated

from fastapi import File
from pydantic import BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]
Picture = Annotated[bytes, BeforeValidator(File)]
