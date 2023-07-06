from typing import Annotated

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.settings import get_sqldb_settings, SQLDBSettings


# sqldb_settings = Annotated[SQLDBSettings, ]
sqldb_settings = get_sqldb_settings()
engine = create_engine(
    sqldb_settings.sql_db_url()
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
