from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse
from fastapi import  Request, FastAPI
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

app = FastAPI()


class ErrorHandlerMiddleware:


    @staticmethod
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        errors = []
        for error in exc.errors():
            errors.append( 
                {
                    "loc": error["loc"],
                    "msg": error["msg"],
                    "type": error["type"],
                }
            )
        return JSONResponse(status_code=HTTP_422_UNPROCESSABLE_ENTITY, content={"detail": errors})

    @staticmethod
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(status_code=exc.status_code, content={"details": exc.detail})

    @staticmethod
    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        return JSONResponse(status_code=500, content={"detail": "Ha ocurrido un error inesperado"})

