from bson import ObjectId
from fastapi import APIRouter, Body, HTTPException, Response, status
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo import ReturnDocument

from database import db
from database.models import AddContest, Contest, ContestsList, UpdateContest

router = APIRouter(prefix="/contests", tags=["Contests"])
contests_collection: AsyncIOMotorCollection = db.get_collection("contests")


@router.get(
    "/get/{id}",
    response_description="Get a single contest",
    response_model=Contest,
    response_model_by_alias=False,
)
async def get_contest(id: str) -> Contest:
    if (
        contest := await contests_collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        return contest

    raise HTTPException(status_code=404, detail=f"Contest {id} not found")


@router.post(
    "/add/",
    response_description="Add new contest",
    response_model=Contest,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def add_contest(contest: AddContest = Body(...)) -> Contest:
    new_contest = await contests_collection.insert_one(contest.model_dump())
    created_contest = await contests_collection.find_one(
        {"_id": new_contest.inserted_id}
    )
    return Contest.model_validate(created_contest)


@router.get(
    "/list/",
    response_description="List all contests",
    response_model=ContestsList,
    response_model_by_alias=False,
)
async def contests_list() -> ContestsList:
    """Показать 1000 записей контестов"""
    return ContestsList(contests=await contests_collection.find().to_list(1000))


@router.put(
    "/update/{id}",
    response_description="Update a contest",
    response_model=Contest,
    response_model_by_alias=False,
)
async def update_contest(id: str, contest: UpdateContest = Body(...)) -> Contest:
    updated_fields = {
        k: v for k, v in contest.model_dump(by_alias=True).items() if v is not None
    }

    if len(updated_fields) >= 1:
        update_result = await contests_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": updated_fields},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"Contest {id} not found")

    # The update is empty, but we should still return the matching document:
    if (
        existing_contest := await contests_collection.find_one({"_id": id})
    ) is not None:
        return existing_contest

    raise HTTPException(status_code=404, detail=f"Contest {id} not found")


# TODO: Мб добавить отдельный поток, с удалением старых конкурсов.
@router.delete("/delete/{id}", response_description="Delete a contest")
async def delete_contest(id: str):
    delete_result = await contests_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Contest {id} not found")
