from fastapi import APIRouter, Body, status
from motor.motor_asyncio import AsyncIOMotorCollection

from database.loader import db
from database.models import AddContest, Contest, ContestsList

router = APIRouter(prefix="/contests")
student_collection: AsyncIOMotorCollection = db.get_collection("contests")


@router.post(
    "/add/",
    response_description="Add new student",
    response_model=Contest,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def add_student(student: AddContest = Body(...)) -> Contest:
    new_student = await student_collection.insert_one(student.model_dump())
    created_student = await student_collection.find_one(
        {"_id": new_student.inserted_id}
    )
    return Contest.model_validate(created_student)


@router.get(
    "/list/",
    response_description="List all contests",
    response_model=ContestsList,
    response_model_by_alias=False,
)
async def contests_list() -> ContestsList:
    "Показать 1000 записей студентов"
    return ContestsList(contests=await student_collection.find().to_list(1000))
