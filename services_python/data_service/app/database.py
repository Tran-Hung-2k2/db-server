from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:postgres@localhost/postgres"


engine = create_engine(DATABASE_URL)
# engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency to get the database session
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
