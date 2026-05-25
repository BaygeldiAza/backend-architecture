from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker, declarative_base
#from app.core.config import settings

SQL_ALCHEMY_URL = 'postgresql://postgres:password1234@localhost/backend-architecture'

engine = create_engine(SQL_ALCHEMY_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base=declarative_base()