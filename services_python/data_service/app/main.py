import os
import sys

sys.path.append(".")

from dotenv import load_dotenv

load_dotenv()

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from services_python.data_service.app.api import router
from services_python.data_service.app.database import engine
from services_python.data_service.app.models import Base
from services_python.utils.exception import MyException, my_exception_handler

Base.metadata.create_all(bind=engine)

app = FastAPI()

ALLOW_ORIGIN = os.getenv("ALLOW_ORIGIN", "http://localhost:5173")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOW_ORIGIN],
    allow_credentials=True,
    allow_methods=["GET", "HEAD", "OPTIONS", "PUT", "PATCH", "POST", "DELETE"],
    allow_headers=[
        "Origin",
        "Content-Length",
        "Content-Type",
        "Access-Control-Allow-Headers",
        "Authorization",
        "Set-Cookie",
    ],
)

app.include_router(router)

app.add_exception_handler(MyException, my_exception_handler)

if __name__ == "__main__":
    uvicorn.run(
        "services_python.data_service.app.main:app",
        host=os.getenv("REST_HOST", "0.0.0.0"),
        port=int(os.getenv("REST_PORT", "8083")),
        reload=True,
    )
