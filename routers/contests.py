from beanie import PydanticObjectId
from bson import ObjectId
from fastapi import APIRouter, HTTPException, Response, status
from pymongo import ReturnDocument

from models import Contest, UpdateContest

router = APIRouter(prefix="/contests", tags=["Contests"])


@router.get(
    "/get/{id}",
    response_description="Get a single contest",
    response_model=Contest,
    response_model_by_alias=False,
)
async def get_contest(id: str) -> Contest:
    if (contest := await Contest.find_one({"_id": ObjectId(id)})) is not None:
        return contest

    raise HTTPException(status_code=404, detail=f"Contest {id} not found")


@router.post(
    "/add/",
    response_description="Add new contest",
    response_model=Contest,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def add_contest(contest: Contest) -> Contest:
    return await contest.insert()


@router.get(
    "/list/",
    response_description="List all contests",
    response_model_by_alias=False,
)
async def contests_list():
    """Показать 1000 записей контестов"""
    return await Contest.find().to_list(1000)


@router.put(
    "/update/{contest_id}",
    response_description="Update a contest",
    response_model=Contest,
    response_model_by_alias=False,
)
async def update_contest(
    contest_id: PydanticObjectId, contest: UpdateContest
) -> Contest:
    old_contest = await Contest.find_one({"_id": contest_id})
    if not old_contest:
        raise HTTPException(status_code=404, detail=f"Contest {id} not found")

    updated_fields = {k: v for k, v in contest.model_dump().items() if v is not None}
    if len(updated_fields) >= 1:
        return await (await old_contest.set(updated_fields)).save()
    else:
        return old_contest


# TODO: Мб добавить отдельный поток, с удалением старых конкурсов.
@router.delete("/delete/{contest_id}", response_description="Delete a contest")
async def delete_contest(contest_id: PydanticObjectId):
    if await Contest.find_one({"_id": contest_id}).delete():
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Contest {id} not found")
