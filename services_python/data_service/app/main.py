import sys

sys.path.append(".")

import uvicorn
from fastapi import FastAPI

from services_python.data_service.app.api.v1 import router
from services_python.data_service.app.database import engine
from services_python.data_service.app.models import Base

# migrate all
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include the user router
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("services_python.data_service.app.main:app", host="127.0.0.1", port=8080, reload=True)
