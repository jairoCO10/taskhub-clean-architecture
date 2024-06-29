# app/core/usecases/user_usecase.py
from typing import List
from app.core.entities.user import User, CreateUser
from app.interface_adapters.gateways.db_gateway import UserGateway

class UserUseCase:
    def __init__(self, user_gateway: UserGateway):
        self.user_gateway = user_gateway

    async def create_user(self, name: str, email: str) -> CreateUser:
        return await self.user_gateway.create_user(name, email)

    async def get_user(self, user_id: int) -> User:
        return await self.user_gateway.get_user(user_id)
    
    async def get_users(self,skip:int, limit:int) -> User:
        return await self.user_gateway.get_users(skip, limit)

    async def update_user(self, user_id: int, name: str, email: str) -> User:
        return await self.user_gateway.update_user(user_id, name, email)

    async def delete_user(self, user_id: int) -> User:
        return await self.user_gateway.delete_user(user_id)