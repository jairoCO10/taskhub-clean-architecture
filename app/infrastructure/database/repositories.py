# app/infrastructure/database/repositories.py
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from app.infrastructure.database.models import Task as ORMTask
from app.infrastructure.database.models import User as ORMUser

class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    async def create_task(self, title: str, description: str, user_id: int) -> ORMTask:
        task = ORMTask(title=title, description=description, user_id=user_id)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    async def get_tasks(self, skip: int = 0, limit: int = 10) -> List[ORMTask]:
        result = self.db.execute(select(ORMTask).offset(skip).limit(limit))
        return result.scalars().all()

    async def get_task(self, task_id: int) -> ORMTask:
        result = self.db.execute(select(ORMTask).filter(ORMTask.id == task_id))
        return result.scalars().first()

    async def update_task(self, task_id: int, title: str, description: str, completed: bool) -> ORMTask:
        task = await self.get_task(task_id)
        if task:
            task.title = title
            task.description = description
            task.completed = completed
            self.db.commit()
            self.db.refresh(task)
        return task

    async def delete_task(self, task_id: int) -> ORMTask:
        task = await self.get_task(task_id)
        if task:
            self.db.delete(task)
            self.db.commit()
        return task



class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    async def create_user(self, name: str, email: str) -> ORMUser:
        user = ORMUser(name=name, email=email)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    async def get_user(self, user_id: int) -> ORMUser:
        result = self.db.execute(select(ORMUser).filter(ORMUser.id == user_id))
        return result.scalars().first()

    async def get_users(self, skip: int, limit: int) -> List[ORMUser]:
        result = self.db.execute(select(ORMUser).offset(skip).limit(limit))
        return result.scalars().all()

    async def update_user(self, user_id: int, name: str, email: str) -> ORMUser:
        user = await self.get_user(user_id)
        if user:
            user.name = name
            user.email = email
            self.db.commit()
            self.db.refresh(user)
        return user

    async def delete_user(self, user_id: int) -> ORMUser:
        user = await self.get_user(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
        return user
    
    async def get_task_user(self, user_id: int) -> List[ORMTask]:
        result = self.db.execute(select(ORMTask).filter(ORMTask.user_id == user_id))
        return result.scalars().all()

