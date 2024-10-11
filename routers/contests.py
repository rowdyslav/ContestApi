from fastapi import APIRouter, Body, status
from motor.motor_asyncio import AsyncIOMotorCollection

from database.loader import db
from database.models import AddContest, Contest, ContestsList

router = APIRouter(prefix="/contests", tags=["Contests"])
contests_collection: AsyncIOMotorCollection = db.get_collection("contests")


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
    "Показать 1000 записей студентов"
    return ContestsList(contests=await contests_collection.find().to_list(1000))
