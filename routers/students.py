from bson import ObjectId
from fastapi import APIRouter, Body, HTTPException, Response, status
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo import ReturnDocument

from database.loader import db
from database.models import AddStudent, Student, StudentsList, UpdateStudent

router = APIRouter(prefix="/students", tags=["Students"])
students_collection: AsyncIOMotorCollection = db.get_collection("students")


@router.get(
    "/get/{id}",
    response_description="Get a single student",
    response_model=Student,
    response_model_by_alias=False,
)
async def get_student(id: str) -> Student:
    if (
        student := await students_collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        return student

    raise HTTPException(status_code=404, detail=f"Student {id} not found")


@router.post(
    "/add/",
    response_description="Add new student",
    response_model=Student,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def add_student(student: AddStudent = Body(...)) -> Student:
    new_student = await students_collection.insert_one(student.model_dump())
    created_student = await students_collection.find_one(
        {"_id": new_student.inserted_id}
    )
    return Student.model_validate(created_student)


@router.get(
    "/list/",
    response_description="List all students",
    response_model=StudentsList,
    response_model_by_alias=False,
)
async def students_list() -> StudentsList:
    "Показать 1000 записей студентов"
    return StudentsList(students=await students_collection.find().to_list(1000))


@router.put(
    "/update/{id}",
    response_description="Update a student",
    response_model=Student,
    response_model_by_alias=False,
)
async def update_student(id: str, student: UpdateStudent = Body(...)) -> Student:
    """
    Update individual fields of an existing student record.

    Only the provided fields will be updated.
    Any missing or `null` fields will be ignored.
    """
    updated_fields = {
        k: v for k, v in student.model_dump(by_alias=True).items() if v is not None
    }

    if len(updated_fields) >= 1:
        update_result = await students_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": updated_fields},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"Student {id} not found")

    # The update is empty, but we should still return the matching document:
    if (
        existing_student := await students_collection.find_one({"_id": id})
    ) is not None:
        return existing_student

    raise HTTPException(status_code=404, detail=f"Student {id} not found")


@router.delete("/delete/{id}", response_description="Delete a student")
async def delete_student(id: str):
    delete_result = await students_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Student {id} not found")
