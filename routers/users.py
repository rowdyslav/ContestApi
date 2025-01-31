from base64 import b64decode, b64encode
from typing import Annotated, List, Optional

from beanie import Link, PydanticObjectId
from bson import DBRef
from fastapi import (
    APIRouter,
    File,
    HTTPException,
    Request,
    Response,
    UploadFile,
    status,
)

from database import fs
from models import UpdateUser, User

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/add/",
    response_description="Add new User",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
)
async def add(user: User) -> User:
    return await user.insert()


@router.get(
    "/get/{user_id}", response_description="Get a single User", response_model=User
)
async def get(user_id: PydanticObjectId) -> User:
    if (user := await User.get(user_id)) is None:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")

    return user


@router.get("/list/", response_description="List all Users", response_model=List[User])
async def list() -> list[User]:
    "Показать 1000 записей студентов"
    return await User.find().to_list(1000)


@router.patch(
    "/update/{user_id}", response_description="Update a user", response_model=User
)
async def update(user_id: PydanticObjectId, user: UpdateUser) -> User:
    if (old_user := await User.get(user_id)) is None:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")

    updated_fields = {k: v for k, v in user.model_dump().items() if v is not None}
    if len(updated_fields) >= 1:
        return await (await old_user.set(updated_fields)).save()
    else:
        return old_user


@router.post("/set_avatar/{user_id}")
async def set_avatar(user_id: PydanticObjectId, user_avatar: UploadFile):
    if (user := await User.get(user_id)) is None:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")

    user.avatar = b64encode(await user_avatar.read()).decode("utf-8")
    return await user.save()


@router.get("/get_avatar/{user_id}")
async def get_avatar(user_id: PydanticObjectId, r: Request):
    if (user := await User.get(user_id)) is None:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    if user.avatar is None:
        return None

    return Response(b64decode(user.avatar), media_type="image/png")


@router.delete(
    "/delete/{user_id}",
    response_description="Delete a User",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(user_id: PydanticObjectId):
    if (user := await User.get(user_id)) is None:
        raise HTTPException(status_code=404, detail=f"User {id} not found")

    await user.delete()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
