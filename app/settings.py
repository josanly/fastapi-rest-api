import os
import sys
from functools import lru_cache

from pydantic import BaseSettings, Field, SecretStr, ValidationError
from app.logger.config import Mode, get_structlogger

SecretsDirEnvVarName: str = 'SECRETS_DIR'


@lru_cache()
def get_secret_dir():
    try:
        return os.environ[SecretsDirEnvVarName]
    except KeyError:
        get_structlogger().error(f"Missing env var: {SecretsDirEnvVarName}")
        sys.exit(1)


class Settings(BaseSettings):
    app_name: str = "FastAPI REST API"
    app_version: str = Field(default="0.1.0", validate_default=True, regex="^[0-9]\\.[0-9]\\.[0-9]")


def build_sql_db_url(user: str, pwd: SecretStr, host: str, db_name: str) -> str:
    return 'postgresql://' \
           + user \
           + ':' \
           + pwd.get_secret_value() \
           + '@' \
           + host \
           + '/' \
           + db_name


class SQLDBSettings(BaseSettings):
    sql_db_name: str
    sql_db_user: str
    sql_db_password: SecretStr
    sql_db_host: str
    sql_db_url: str = 'to_define'

    class Config:
        secrets_dir: str = get_secret_dir()

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        if self.sql_db_url == 'to_define':
            self.sql_db_url = build_sql_db_url(self.sql_db_user,
                                               self.sql_db_password,
                                               self.sql_db_host,
                                               self.sql_db_name)


class DocumentDBSettings(BaseSettings):
    mongo_db_name:      str
    mongo_db_user:      str
    mongo_db_password:  SecretStr
    mongo_db_host:      str
    # mongo_db_host: str = Field(..., env='MONGO_DB_HOST')
    # Field not required if the env var has the same name (case not sensitive by default)

    class Config:
        secrets_dir = get_secret_dir()

    def mongo_db_url(self) -> str:
        return 'mongodb://' \
            + self.mongo_db_user \
            + ':' \
            + self.mongo_db_password.get_secret_value() \
            + '@' \
            + self.mongo_db_host \
            + '/' \
            + self.mongo_db_name \
            + '?retryWrites=true&w=majority'

# export MONGODB_URL="mongodb+srv://<username>:<password>@<url>/<db>?retryWrites=true&w=majority"


class LoggerSettings(BaseSettings):
    mode: Mode = Field(default=Mode.full, validate_default=True, env='LOG_MODE')


@lru_cache()
def get_mongodb_settings():
    try:
        mongodb_settings = DocumentDBSettings()
    except ValidationError as error:
        get_structlogger().error("Catch Validation Error during configuration of application", errors=error.errors())
        sys.exit(1)
    except RuntimeError as error:
        get_structlogger().error("Fatal exception during configuration of application", errors=error)
        sys.exit(1)
    else:
        get_structlogger().info("Settings", mongodb_settings=mongodb_settings, mongodb_url=mongodb_settings.mongo_db_url())
        return mongodb_settings


@lru_cache()
def get_sqldb_settings():
    try:
        sqldb_settings = SQLDBSettings()
    except ValidationError as error:
        get_structlogger().error("Catch Validation Error during configuration of application", errors=error.errors())
        sys.exit(1)
    except RuntimeError as error:
        get_structlogger().error("Fatal exception during configuration of application", errors=error)
        sys.exit(1)
    else:
        get_structlogger().info("Settings", sqldb_settings=sqldb_settings)
        return sqldb_settings


@lru_cache()
def get_logger_settings():
    try:
        logger_settings = LoggerSettings()
    except ValidationError as error:
        get_structlogger().error("Catch Validation Error during configuration of application", errors=error.errors())
        sys.exit(1)
    except RuntimeError as error:
        get_structlogger().error("Fatal exception during configuration of application", errors=error)
        sys.exit(1)
    else:
        get_structlogger().info("Settings", logger_settings=logger_settings)
        return logger_settings
