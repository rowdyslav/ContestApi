from typing import Annotated

from PIL import Image
from pydantic import BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]
Picture = Annotated[bytes, lambda f: Image.open(f).verify()]
