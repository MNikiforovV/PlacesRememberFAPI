from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from .settings import Settings

settings = Settings()

SQLALCHEMY_DATABASE_URL = settings.sqlalchemy_database_url

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
