from typing import Annotated

from fastapi import File
from pydantic import BeforeValidator

from validator import validator_picture

PyObjectId = Annotated[str, BeforeValidator(str)]
Picture = Annotated[bytes, BeforeValidator(lambda picture:validator_picture(picture))]
Archive = Annotated[bytes, File]
