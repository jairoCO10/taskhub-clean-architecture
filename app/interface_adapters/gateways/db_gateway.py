# app/interface_adapters/gateways/db_gateway.py
from typing import List
from sqlalchemy.orm import Session
from app.core.entities.task import Task
from app.infrastructure.database.models import Task as ORMTask
from app.infrastructure.database.repositories import TaskRepository
from app.core.entities.user import User, CreateUser
from app.infrastructure.database.models import User as ORMUser
from app.infrastructure.database.repositories import UserRepository

class TaskGateway:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.repository = TaskRepository(self.db_session)

    async def create_task(self, title: str, description: str, user_id: int) -> Task:
        orm_task = await self.repository.create_task(title, description, user_id)
        return Task(id=orm_task.id, title=orm_task.title, description=orm_task.description, completed=orm_task.completed, user_id=orm_task.user_id)

    async def get_tasks(self, skip: int = 0, limit: int = 10) -> List[Task]:
        orm_tasks = await self.repository.get_tasks(skip, limit)
        return [Task(id=task.id, title=task.title, description=task.description, completed=task.completed, user_id=task.user_id) for task in orm_tasks]

    async def get_task(self, task_id: int) -> Task:
        orm_task = await self.repository.get_task(task_id)
        return Task(id=orm_task.id, title=orm_task.title, description=orm_task.description, completed=orm_task.completed, user_id=orm_task.user_id)

    async def update_task(self, task_id: int, title: str, description: str, completed: bool) -> Task:
        orm_task = await self.repository.update_task(task_id, title, description, completed)
        return Task(id=orm_task.id, title=orm_task.title, description=orm_task.description, completed=orm_task.completed, user_id=orm_task.user_id)

    async def delete_task(self, task_id: int) -> Task:
        orm_task = await self.repository.delete_task(task_id)
        return Task(id=orm_task.id, title=orm_task.title, description=orm_task.description, completed=orm_task.completed, user_id=orm_task.user_id)


class UserGateway:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.repository = UserRepository(self.db_session)
        
    async def create_user(self, name: str, email: str) -> CreateUser:
        orm_user = await self.repository.create_user(name, email)
        return CreateUser(id=orm_user.id, name=orm_user.name, email=orm_user.email)

    async def get_user(self, user_id: int) -> User:
        orm_user = await self.repository.get_user(user_id)
        if orm_user:
            tasks =await self.get_task_user(orm_user.id)
            print(tasks)
            return User(id=orm_user.id, name=orm_user.name, email=orm_user.email, tasks=tasks)
        return None

    async def get_users(self, skip: int, limit: int) -> List[User]:
        orm_users = await self.repository.get_users(skip, limit)
        users = []
        for orm_user in orm_users:
            tasks = await self.get_task_user(orm_user.id)
            users.append(User(id=orm_user.id, name=orm_user.name, email=orm_user.email, tasks=tasks))
        return users

    async def update_user(self, user_id: int, name: str, email: str) -> User:
        orm_user = await self.repository.update_user(user_id, name, email)
        if orm_user:
            return User(id=orm_user.id, name=orm_user.name, email=orm_user.email)
        return None

    async def delete_user(self, user_id: int) -> User:
        orm_user = await self.repository.delete_user(user_id)
        if orm_user:
            return User(id=orm_user.id, name=orm_user.name, email=orm_user.email)
        return None
    
    async def get_task_user(self, user_id: int) -> List[Task]:
        orm_tasks = await self.repository.get_task_user(user_id)
        if orm_tasks:
            return [Task(id=task.id, title=task.title, description=task.description, completed=task.completed, user_id=task.user_id) for task in orm_tasks]
        return []