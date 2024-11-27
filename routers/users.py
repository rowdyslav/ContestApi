from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, Path, Response, status
from pymongo import ReturnDocument

from models import UpdateUser, User

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/get/{user_id}",
    response_description="Get a single User",
    response_model=User,
    response_model_by_alias=False,
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
    response_model_by_alias=False,
)
async def add_user(user: User) -> User:
    return await User(**user.model_dump()).insert()


@router.get(
    "/list/",
    response_description="List all Users",
    response_model=List[User],
    response_model_by_alias=False,
)
async def users_list():
    "Показать 1000 записей студентов"
    return await User.find().to_list(1000)


@router.put(
    "/update/{id}",
    response_description="Update a User",
    response_model=User,
    response_model_by_alias=False,
)
async def update_user(user_id: PydanticObjectId, user: UpdateUser) -> User:
    """
    Update individual fields of an existing User record.

    Only the provided fields will be updated.
    Any missing or `null` fields will be ignored.
    """
    updated_fields = {
        k: v for k, v in user.model_dump(by_alias=True).items() if v is not None
    }

    if len(updated_fields) >= 1:
        update_result = await User.find_one_and_update(
            {"_id": user_id},
            {"$set": updated_fields},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"User {id} not found")

    # The update is empty, but we should still return the matching document:
    if (existing_user := await User.find_one({"_id": id})) is not None:
        return existing_user

    raise HTTPException(status_code=404, detail=f"User {id} not found")


@router.delete("/delete/{id}", response_description="Delete a User")
async def delete_user(id: str):
    delete_result = await User.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"User {id} not found")
