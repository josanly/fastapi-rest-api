from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.config import databases_settings

engine = create_engine(
    databases_settings.sql_db_url
)

SessionLocal = sessionmaker(autocommit=False,
                            autoflush=False,
                            bind=engine)

Base = declarative_base()


def get_relationaldb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
