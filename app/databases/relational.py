from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.settings import get_sqldb_settings


engine = create_engine(
    get_sqldb_settings().sql_db_url
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
