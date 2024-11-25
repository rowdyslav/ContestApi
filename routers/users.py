from bson import ObjectId
from fastapi import APIRouter, HTTPException, Response, status
from pymongo import ReturnDocument

from models import AddUser, UpdateUser, User

from . import users_collection

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/get/{id}",
    response_description="Get a single User",
    response_model=User,
    response_model_by_alias=False,
)
async def get_user(id: str) -> User:
    if (user := await users_collection.find_one({"_id": ObjectId(id)})) is not None:
        return user

    raise HTTPException(status_code=404, detail=f"User {id} not found")


@router.post(
    "/add/",
    response_description="Add new User",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def add_user(user: AddUser) -> User:
    inserted_user = await users_collection.insert_one(user.model_dump(by_alias=True))
    q = {"_id": inserted_user.inserted_id}
    new_user = User.model_validate(await users_collection.find_one(q))
    await users_collection.find_one_and_update(
        q, {"$set": new_user.model_dump(exclude={"id"})}
    )
    return new_user


@router.get(
    "/list/",
    response_description="List all Users",
    response_model_by_alias=False,
)
async def users_list():
    "Показать 1000 записей студентов"
    return await users_collection.find().to_list(1000)


@router.put(
    "/update/{id}",
    response_description="Update a User",
    response_model=User,
    response_model_by_alias=False,
)
async def update_user(id: str, user: UpdateUser) -> User:
    """
    Update individual fields of an existing User record.

    Only the provided fields will be updated.
    Any missing or `null` fields will be ignored.
    """
    updated_fields = {
        k: v for k, v in user.model_dump(by_alias=True).items() if v is not None
    }

    if len(updated_fields) >= 1:
        update_result = await users_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": updated_fields},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"User {id} not found")

    # The update is empty, but we should still return the matching document:
    if (existing_user := await users_collection.find_one({"_id": id})) is not None:
        return existing_user

    raise HTTPException(status_code=404, detail=f"User {id} not found")


@router.delete("/delete/{id}", response_description="Delete a User")
async def delete_user(id: str):
    delete_result = await users_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"User {id} not found")
