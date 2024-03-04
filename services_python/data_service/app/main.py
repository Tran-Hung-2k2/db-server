import os
import sys

sys.path.append(".")

from dotenv import load_dotenv

# migrate all# Tải giá trị từ file .env vào biến môi trường
load_dotenv()

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from services_python.data_service.app.api.v1 import router
from services_python.data_service.app.database import engine
from services_python.data_service.app.models import Base
from services_python.utils.exception import MyException, my_exception_handler


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # allow_origins=['myfrontend.com'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
