from bson import ObjectId
from fastapi import APIRouter, Body, HTTPException, Response, status
from pymongo import ReturnDocument

from models import AddProject, Project, ProjectsList, UpdateProject, User

from . import projects_collection, users_collection

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get(
    "/get/{id}",
    response_description="Get a single project",
    response_model=Project,
    response_model_by_alias=False,
)
async def get_project(id: str) -> Project:
    if (
        project := await projects_collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        return project

    raise HTTPException(status_code=404, detail=f"Project {id} not found")


@router.post(
    "/add/",
    response_description="Add new project",
    response_model=Project,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def add_project(project: AddProject) -> Project:
    inserted_project = await projects_collection.insert_one(
        project.model_dump(by_alias=True)
    )
    q = {"_id": inserted_project.inserted_id}
    new_project = Project.model_validate(await projects_collection.find_one(q))
    await projects_collection.find_one_and_update(
        q, {"$set": new_project.model_dump(exclude={"id"})}
    )
    return new_project


@router.get(
    "/list/",
    response_description="List all projects",
    response_model=ProjectsList,
    response_model_by_alias=False,
)
async def projects_list() -> ProjectsList:
    """Показать 1000 записей проектов"""
    return ProjectsList(value=await projects_collection.find().to_list(1000))


@router.get(
    "/list/boosts",
    response_description="List all projects sorted by boosts",
    response_model=ProjectsList,
    response_model_by_alias=False,
)
async def projects_list_boosts() -> ProjectsList:
    """Возвращает список проектов, отсортированных по количеству бустов"""
    sort_key = lambda project: project["boosts"]
    return ProjectsList(
        value=sorted(
            await projects_collection.find().to_list(1000),
            key=sort_key,
            reverse=True,
        )
    )


@router.put(
    "/update/{id}",
    response_description="Update a project",
    response_model=Project,
    response_model_by_alias=False,
)
async def update_project(id: str, project: UpdateProject) -> Project:
    updated_fields = {
        k: v for k, v in project.model_dump(by_alias=True).items() if v is not None
    }

    if len(updated_fields) >= 1:
        update_result = await projects_collection.find_one_and_update(
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
        existing_project := await projects_collection.find_one({"_id": id})
    ) is not None:
        return existing_project

    raise HTTPException(status_code=404, detail=f"Project {id} not found")


@router.put(
    "/boost/{id}",
    response_description="Забустить проект",
)
async def boost_project(id: str, user: User) -> int:
    if not bool(
        user == User.model_validate(await users_collection.find_one(ObjectId(user.id)))
    ):
        raise HTTPException(status_code=404, detail=f"User not found")

    project = Project.model_validate(
        await projects_collection.find_one({"_id": ObjectId(id)})
    )
    if user.id in (member_id for member_id in project.users_ids.value):
        raise HTTPException(
            status_code=409,
            detail=f"User {user.id} is member of Project {id}. Cannot boost your own project",
        )

    update_result = await projects_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$inc": {"boosts": 1}},
        return_document=ReturnDocument.AFTER,
    )
    if update_result is not None:
        return update_result["boosts"]
    else:
        raise HTTPException(status_code=404, detail=f"Project {id} not found")


# TODO: Мб добавить отдельный поток, с удалением старых конкурсов.
@router.delete("/delete/{id}", response_description="Delete a project")
async def delete_project(id: str):
    delete_result = await projects_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Project {id} not found")
