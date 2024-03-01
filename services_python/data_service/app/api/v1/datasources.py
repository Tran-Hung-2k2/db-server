from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from services_python.data_service.app.schemas import User, UserCreate
from services_python.data_service.app.database import get_session

router = APIRouter(prefix="/datasources", tags=["Datasources"])


@router.get("/{user_id}", response_model=User)
async def read_user(db: Session = Depends(get_session)):
    return ""


@router.post("/", response_model=User)
async def create_user(user: UserCreate, db: Session = Depends(get_session)):
    return ""


@router.put("/{user_id}", response_model=User)
async def update_user(
    user_id: int, user: UserCreate, db: Session = Depends(get_session)
):
    return ""


@router.delete("/{user_id}", response_model=User)
async def delete_user(user_id: int, db: Session = Depends(get_session)):
    return ""
