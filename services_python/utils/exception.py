from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse


class MyException(HTTPException):
    pass


def my_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail, "detail": exc.detail},
    )
