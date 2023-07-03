from typing import Union
from fastapi import FastAPI

from .databases.relational import Base, engine
from .routers import auth, users
from .config import databases_settings

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(users.router)

# debug routes


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/settings")
def db_info():
    return databases_settings.sql_db_url