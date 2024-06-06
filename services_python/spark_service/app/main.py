import os
import sys

sys.path.append(".")

from dotenv import load_dotenv  # type: ignore

load_dotenv()

import uvicorn  # type: ignore
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from services_python.mage_service.app.api import router

# from services_python.mage_service.app.database import engine
# from services_python.mage_service.app.models import Base
from services_python.utils.exception import MyException, my_exception_handler
from services_python.middlewares.cors import add_cors_middleware


# Base.metadata.create_all(bind=engine)

app = FastAPI()

add_cors_middleware(app)

app.include_router(router)

app.add_exception_handler(MyException, my_exception_handler)

if __name__ == "__main__":
    uvicorn.run(
        "services_python.mage_service.app.main:app",
        host=os.getenv("REST_HOST", "0.0.0.0"),
        port=int(os.getenv("REST_PORT", "8086")),
        reload=True,
    )
