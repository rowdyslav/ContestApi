from bson import ObjectId
from fastapi import APIRouter, Body, HTTPException, Response, status
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo import ReturnDocument

from database.loader import db
from database.models import AddProject, Project, ProjectsList, UpdateProject

router = APIRouter(prefix="/projects", tags=["Projects"])
project_collection: AsyncIOMotorCollection = db.get_collection("projects")


@router.get(
    "/get/{id}",
    response_description="Get a single project",
    response_model=Project,
    response_model_by_alias=False,
)
async def get_project(id: str) -> Project:
    if (
        contest := await project_collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        return contest

    raise HTTPException(status_code=404, detail=f"Project {id} not found")

@router.get(
    "/list/",
    response_description="List all projects",
    response_model=ProjectsList,
    response_model_by_alias=False,
)
async def projects_list() -> ProjectsList:
    """Показать 1000 записей контестов"""
    return ProjectsList(projects=await project_collection.find().to_list(1000))

@router.post(
    "/add/",
    response_description="Add new project",
    response_model=Project,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def add_project(project: AddProject = Body(...)) -> Project:
    new_project = await project_collection.insert_one(project.model_dump())
    created_project = await project_collection.find_one(
        {"_id": new_project.inserted_id}
    )
    return Project.model_validate(created_project)

@router.put(
    "/update/{id}",
    response_description="Update a contest",
    response_model=Project,
    response_model_by_alias=False,
)
async def update_project(id: str, project: UpdateProject = Body(...)) -> Project:
    updated_fields = {
        k: v for k, v in project.model_dump(by_alias=True).items() if v is not None
    }

    if len(updated_fields) >= 1:
        update_result = await project_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": updated_fields},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"Project {id} not found")

    # The update is empty, but we should still return the matching document:
    if (
        existing_contest := await project_collection.find_one({"_id": id})
    ) is not None:
        return existing_contest

    raise HTTPException(status_code=404, detail=f"Project {id} not found")


# TODO: Мб добавить отдельный поток, с удалением старых конкурсов.
@router.delete("/delete/{id}", response_description="Delete a project")
async def delete_project(id: str):
    delete_result = await project_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Project {id} not found")
