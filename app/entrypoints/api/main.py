# app/entrypoints/api/main.py
from fastapi import FastAPI
from app.infrastructure.database import Connection
from app.entrypoints.api.middleware import ErrorHandlerMiddleware
from app.interface_adapters.controllers import task_controller
from app.interface_adapters.controllers import user_controller


Connection.Base.metadata.create_all(bind=Connection.engine)

app = FastAPI()

# Registra el middleware de manejo de errores
# app.add_middleware(ErrorHandlerMiddleware)



app.include_router(task_controller.router, prefix="/api/v1/tasks", tags=["tasks"])
app.include_router(user_controller.router, prefix="/api/v1/users", tags=["users"])

