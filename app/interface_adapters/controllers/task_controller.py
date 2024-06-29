# app/interface_adapters/controllers/task_controller.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.usecases.task_usecase import TaskUseCase
from app.interface_adapters.gateways.db_gateway import TaskGateway
from app.infrastructure.database import Connect
from app.entrypoints.api.schemas import TaskCreate, TaskRead, TaskUpdate

router = APIRouter()

@router.post("/tasks/", response_model=TaskRead)
async def create_task(task: TaskCreate, db: AsyncSession = Depends(Connect.get_db)):
    task_gateway = TaskGateway(db)
    task_usecase = TaskUseCase(task_gateway)
    return await task_usecase.create_task(task.title, task.description, task.user_id)


@router.get("/tasks/", response_model=List[TaskRead])
async def read_tasks(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(Connect.get_db)):
    task_gateway = TaskGateway(db)
    task_usecase = TaskUseCase(task_gateway)
    return await task_usecase.get_tasks(skip, limit)

@router.get("/tasks/{task_id}", response_model=TaskRead)
async def read_task(task_id: int, db: AsyncSession = Depends(Connect.get_db)):
    task_gateway = TaskGateway(db)
    task_usecase = TaskUseCase(task_gateway)
    task = await task_usecase.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/tasks/{task_id}", response_model=TaskRead)
async def update_task(task_id: int, task: TaskUpdate, db: AsyncSession = Depends(Connect.get_db)):
    task_gateway = TaskGateway(db)
    task_usecase = TaskUseCase(task_gateway)
    updated_task = await task_usecase.update_task(task_id, task.title, task.description, task.completed)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@router.delete("/tasks/{task_id}", response_model=TaskRead)
async def delete_task(task_id: int, db: AsyncSession = Depends(Connect.get_db)):
    task_gateway = TaskGateway(db)
    task_usecase = TaskUseCase(task_gateway)
    deleted_task = await task_usecase.delete_task(task_id)
    if not deleted_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return deleted_task
