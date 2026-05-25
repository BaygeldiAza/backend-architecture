from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker, declarative_base
#from app.core.config import settings

SQL_ALCHEMY_URL = "postgresql://postgres:password@localhost:5432/backend-architecture"

engine = create_engine(SQL_ALCHEMY_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base=declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
