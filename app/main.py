from typing import Union
from fastapi import FastAPI, Depends
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.staticfiles import StaticFiles

from .databases.document import mongodb_settings
from .databases.relational import Base, engine, sqldb_settings
from .logger.config import Mode, StructLoggingMiddleware, get_structlogger
from .routers import auth, users, analyses
from .settings import get_logger_settings, get_sqldb_settings, get_mongodb_settings


app = FastAPI()

# Log management
app.add_middleware(StructLoggingMiddleware, mode=get_logger_settings().mode)

# Relational DB
Base.metadata.create_all(bind=engine)

# Add static files
# app.mount("/static", StaticFiles(directory="static"), name="static")

# Routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(analyses.router)


@app.get("/health", status_code=status.HTTP_200_OK)
async def app_healthy(logger=Depends(get_structlogger)):
    logger.info("Check status of application")
    return {"state": "healthy"}


@app.get("/")
def read_root(logger=Depends(get_structlogger)):
    logger.info("Hello World info")
    logger.info({"message": "json as main log"})
    logger.debug("Debuuuug", foo="foo", bar="bar")
    logger.error("Erroooor!!!", obj={"foo": "bar"}, test="test")
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/settings")
def settings(logger=Depends(get_structlogger)):
    logger_settings = get_logger_settings()
    logger.info("GET Settings",
                sqldb_settings=jsonable_encoder(sqldb_settings.dict()),
                mongodb_settings=jsonable_encoder(mongodb_settings.dict()),
                logger_settings=jsonable_encoder(logger_settings.dict()))
    return {
        'sqldb_settings': sqldb_settings.dict(),
        'mongodb_settings': mongodb_settings.dict(),
        'logger_settings': logger_settings.dict()
    }
