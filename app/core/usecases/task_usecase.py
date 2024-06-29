from typing import List
from app.core.entities.task import Task
from app.interface_adapters.gateways.db_gateway import TaskGateway

class TaskUseCase:
    def __init__(self, task_gateway: TaskGateway):
        self.task_gateway = task_gateway

    async def create_task(self, title: str, description: str, user_id: int) -> Task:
        return await self.task_gateway.create_task(title, description, user_id)

    async def get_tasks(self, skip: int = 0, limit: int = 10) -> List[Task]:
        return await self.task_gateway.get_tasks(skip, limit)

    async def get_task(self, task_id: int) -> Task:
        return await self.task_gateway.get_task(task_id)

    async def update_task(self, task_id: int, title: str, description: str, completed: bool) -> Task:
        return await self.task_gateway.update_task(task_id, title, description, completed)

    async def delete_task(self, task_id: int) -> Task:
        return await self.task_gateway.delete_task(task_id)