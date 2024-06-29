# app/entrypoints/api/schemas.py
from pydantic import BaseModel
from typing import List, Optional

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None

class TaskCreate(TaskBase):
    user_id: int

class TaskUpdate(TaskBase):
    completed: bool

class TaskRead(TaskBase):
    id: int
    completed: bool
    user_id: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int
    tasks: List[TaskRead] = []

    class Config:
        from_attributes = True
