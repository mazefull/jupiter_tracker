from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, FastAPI

from config import settings
from db.db import reset_db
from schemas.pydantic_schema import SRTaskAddSchema, SDAddSchema
from services.initial_manager import ManagerService, ManagerSD


router_sr = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

router_sd = APIRouter(
    prefix="/sd",
    tags=["sd"]
)

router_main = APIRouter(
    prefix="",
    tags=["main"]
)
#

@router_sr.post("/setup_db", summary='HARD RESET DB')
async def setup_db():
    return await reset_db()


@router_sr.post("/new_task")
async def create_task(task: SRTaskAddSchema):
    result = await ManagerService().new_task(task)
    print("11 ", result)
    if result["ok"] is False:
        raise HTTPException(status_code=423, detail=result)
    else:
        return result


@router_sd.post("/new_sd")
async def create_sd(sd: SDAddSchema):
    result = await ManagerSD().new_sd(sd)
    return result



@router_sr.get("/get_projects", summary='Get all projects and their thematics')
async def get_projects(service: Annotated[ManagerService, Depends(ManagerService)]):
    result = await service.get_projects_data()
    return {"projects": result}

@router_main.get("/")
async def mainpage():
    return {"hello": f"Follow to {settings.FASTAPI_HOST}:8000/docs"}