from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from .config import settings

DB_URL = (
    f"postgresql://"
    f"{settings.DB_USER}:"
    f"{settings.PASSWORD}@"
    f"{settings.HOST}/"
    f"{settings.DATABASE}"
)


engine = create_engine(DB_URL)

SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()