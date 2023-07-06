from functools import lru_cache
from typing import Annotated

from fastapi import FastAPI, Depends
from fastapi_healthcheck import HealthCheckFactory, healthCheckRoute
from starlette import status

from .databases.relational import Base, engine
from .logger.config import StructLoggingMiddleware, get_structlogger
from .routers import auth, users, analyses
from .settings import Settings, LoggerSettings, DocumentDBSettings, get_mongodb_settings, \
    get_sqldb_settings, get_logger_settings, SQLDBSettings


app = FastAPI()


@lru_cache()
def get_settings():
    return Settings()


# Log management
app.add_middleware(StructLoggingMiddleware, mode=get_logger_settings().mode)

# Add Health Checks
_healthChecks = HealthCheckFactory()

# Relational DB
Base.metadata.create_all(bind=engine)

# Add static files
# app.mount("/static", StaticFiles(directory="static"), name="static")

# Routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(analyses.router)
app.add_api_route('/health', endpoint=healthCheckRoute(factory=_healthChecks), tags=["application"])


@app.get("/info", status_code=status.HTTP_200_OK, tags=["application"])
async def info(app_settings: Annotated[Settings, Depends(get_settings)], logger=Depends(get_structlogger)):
    app_info = {
        "app_name": app_settings.app_name,
        "version":  app_settings.app_version
    }
    logger.info("Application information", info=app_info)
    return app_info

