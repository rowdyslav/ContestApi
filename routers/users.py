from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, Response, status

from models import UpdateUser, User

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/get/{user_id}", response_description="Get a single User", response_model=User
)
async def get_user(user_id: PydanticObjectId) -> User:
    if (user := await User.find_one({"_id": user_id})) is not None:
        return user

    raise HTTPException(status_code=404, detail=f"User {user_id} not found")


@router.post(
    "/add/",
    response_description="Add new User",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
)
async def add_user(user: User) -> User:
    return await user.insert()


@router.get("/list/", response_description="List all Users", response_model=List[User])
async def users_list():
    "Показать 1000 записей студентов"
    return await User.find().to_list(1000)


@router.put(
    "/update/{user_id}", response_description="Update a user", response_model=User
)
async def update_user(user_id: PydanticObjectId, user: UpdateUser) -> User:
    old_user = await User.find_one({"_id": user_id})
    if not old_user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")

    updated_fields = {k: v for k, v in user.model_dump().items() if v is not None}
    if len(updated_fields) >= 1:
        return await (await old_user.set(updated_fields)).save()
    else:
        return old_user


@router.delete("/delete/{user_id}", response_description="Delete a User")
async def delete_user(user_id: PydanticObjectId):
    if await User.find_one({"_id": user_id}).delete():
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"User {id} not found")
