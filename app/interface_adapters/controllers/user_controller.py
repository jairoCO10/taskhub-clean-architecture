# app/interface_adapters/controllers/user_controller.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.usecases.user_usecase import UserUseCase
from app.interface_adapters.gateways.db_gateway import UserGateway
from app.infrastructure.database import Connect
from app.entrypoints.api.schemas import UserCreate, UserRead

router = APIRouter()

@router.post("/users/", response_model=UserRead)
async def create_user(user: UserCreate, db: Session = Depends(Connect.get_db)):
    user_gateway = UserGateway(db)
    user_usecase = UserUseCase(user_gateway)
    return await user_usecase.create_user(user.name, user.email)

@router.get("/users/", response_model=List[UserRead])
async def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(Connect.get_db)):
    user_gateway = UserGateway(db)
    user_usecase = UserUseCase(user_gateway)
    return await user_usecase.get_users(skip, limit)

@router.get("/users/{user_id}", response_model=UserRead)
async def read_user(user_id: int, db: Session = Depends(Connect.get_db)):
    user_gateway = UserGateway(db)
    user_usecase = UserUseCase(user_gateway)
    user = await user_usecase.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{user_id}", response_model=UserRead)
async def update_user(user_id: int, user: UserCreate, db: Session = Depends(Connect.get_db)):
    user_gateway = UserGateway(db)
    user_usecase = UserUseCase(user_gateway)
    updated_user = await user_usecase.update_user(user_id, user.name, user.email)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/users/{user_id}", response_model=UserRead)
async def delete_user(user_id: int, db: Session = Depends(Connect.get_db)):
    user_gateway = UserGateway(db)
    user_usecase = UserUseCase(user_gateway)
    deleted_user = await user_usecase.delete_user(user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    return deleted_user
