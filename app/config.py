import os
import sys

from fastapi import Depends
from pydantic import BaseSettings, Field, SecretStr

from app.logger.config import Mode, get_structlogger

secrets_dir: str = 'SECRETS_DIR'


def get_secret_dir():
    try:
        return os.environ[secrets_dir]
    except KeyError:
        get_structlogger().error(f"Missing env var: {secrets_dir}")
        sys.exit(1)




class SQLDBSettings(BaseSettings):
    sql_db_name:     str = Field(..., env='SQL_DB_NAME')
    sql_db_user:     str = Field(..., env='SQL_DB_USER')
    sql_db_password: SecretStr
    sql_db_host:     str = Field(..., env='SQL_DB_HOST')

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
    mongo_db_name:      str = Field(..., env='MONGO_DB_NAME')
    mongo_db_user:      str = Field(..., env='MONGO_DB_USER')
    mongo_db_password:  SecretStr
    mongo_db_host:      str = Field(..., env='MONGO_DB_HOST')

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

#export MONGODB_URL="mongodb+srv://<username>:<password>@<url>/<db>?retryWrites=true&w=majority"


class LoggerSettings(BaseSettings):
    mode: Mode = Field(default=Mode.full, validate_default=True, env='LOG_MODE')


sqldb_settings = SQLDBSettings()
mongodb_settings = DocumentDBSettings()
logger_settings = LoggerSettings()


