from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from db.db import reset_db
from schemas.pydantic_schema import SRTaskAddSchema
from services.initial_manager import ManagerService

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)


# SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.post("/setup_db", summary='HARD RESET DB')
async def setup_db():
    return await reset_db()


@router.post("/new_task")
async def create_task(task: SRTaskAddSchema):
    result = await ManagerService().new_task(task)
    raise HTTPException(status_code=result.status_code, detail=result.details)


@router.get("/get_projects", summary='Get all projects and their thematics')
async def get_projects(service: Annotated[ManagerService, Depends(ManagerService)]):
    result = await service.get_projects_data()
    return {"projects": result}
