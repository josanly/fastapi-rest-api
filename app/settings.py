import os
import sys

from pydantic import BaseSettings, Field, SecretStr, ValidationError

from app.logger.config import Mode, get_structlogger

secrets_dir: str = 'SECRETS_DIR'


def get_secret_dir():
    try:
        return os.environ[secrets_dir]
    except KeyError:
        get_structlogger().error(f"Missing env var: {secrets_dir}")
        sys.exit(1)


class SQLDBSettings(BaseSettings):
    sql_db_name: str
    sql_db_user: str
    sql_db_password: SecretStr
    sql_db_host: str

    class Config:
        secrets_dir = get_secret_dir()

    @property
    def sql_db_url(self):
        return 'postgresql://' \
               + self.sql_db_user \
               + ':' \
               + self.sql_db_password.get_secret_value() \
               + '@' \
               + self.sql_db_host \
               + '/' \
               + self.sql_db_name


class DocumentDBSettings(BaseSettings):
    mongo_db_name:      str
    mongo_db_user:      str
    mongo_db_password:  SecretStr
    mongo_db_host:      str
    # mongo_db_host: str = Field(..., env='MONGO_DB_HOST')
    # Field not required if the env var has the same name (case not sensitive by default)

    class Config:
        secrets_dir = get_secret_dir()

    @property
    def mongo_db_url(self):
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
        get_structlogger().info("Settings", mongodb_settings=mongodb_settings)
        return mongodb_settings
