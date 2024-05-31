import sys

sys.path.append(".")

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from services_python.ml_service.app.api import router
from services_python.ml_service.app.models import Base
from services_python.ml_service.app.database import engine

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Machine Learning Operation (MLOps) - Data Enablement Platform (VHT)",
    description="This is a very fancy project, with auto docs for the API and everything",
    version="0.0.0",
)

from starlette.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "services_python.ml_service.app.main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
    )
