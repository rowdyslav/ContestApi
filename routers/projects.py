from beanie import PydanticObjectId
from bson import ObjectId
from fastapi import APIRouter, HTTPException, Response, status

from models import Project, UpdateProject, User

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("/get/{id}", response_model=Project)
async def get_project(id: str) -> Project:
    if (project := await Project.find_one({"_id": ObjectId(id)})) is not None:
        return project

    raise HTTPException(status_code=404, detail=f"Project {id} not found")


@router.post(
    "/add/",
    response_description="New project",
    response_model=Project,
    status_code=status.HTTP_201_CREATED,
)
async def add_project(project: Project) -> Project:
    return await project.insert()


@router.get("/list/", response_description="List all projects")
async def projects_list() -> list[Project]:
    """Показать 1000 записей проектов"""
    return await Project.find().to_list(1000)


@router.get("/list/boosts", response_description="List all projects sorted by boosts")
async def projects_list_boosts():
    """Возвращает список проектов, отсортированных по количеству бустов"""
    return sorted(
        await Project.find().to_list(1000), key=lambda project: ~project.boosts
    )


@router.patch(
    "/update/{project_id}",
    response_description="Updated project",
    response_model=Project,
)
async def update_project(
    project_id: PydanticObjectId, project: UpdateProject
) -> Project:
    old_project = await Project.find_one({"_id": project_id})
    if not old_project:
        raise HTTPException(status_code=404, detail=f"Project {id} not found")

    updated_fields = {k: v for k, v in project.model_dump().items() if v is not None}
    if len(updated_fields) >= 1:
        return await (await old_project.set(updated_fields)).save()
    else:
        return old_project


@router.put("/boost/{project_id}", response_description="New boosts count")
async def boost_project(project_id: PydanticObjectId, user: User) -> int:
    if not bool(user == User.model_validate(await User.find_one({"_id": user.id}))):
        raise HTTPException(status_code=404, detail=f"User not found or not valid")

    project = await Project.find_one({"_id": project_id})
    if not project:
        raise HTTPException(status_code=404, detail=f"Project {project_id} not found")
    if user in project.users:
        raise HTTPException(
            status_code=409,
            detail=f"User {user.id} is member of Project {project_id}. Boosting your own projects is prohibited",
        )
    await (await project.inc({"boosts": 1})).save()
    return project.boosts


@router.delete("/delete/{project_id}")
async def delete_project(project_id: PydanticObjectId):
    if await Project.find_one({"_id": project_id}).delete():
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Project {id} not found"
    )
