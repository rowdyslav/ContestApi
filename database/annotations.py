from typing import Annotated

from fastapi import File
from PIL import Image
from pydantic import BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]
Picture = Annotated[bytes, lambda f: Image.open(f).verify()]
Files = Annotated[bytes, File]
