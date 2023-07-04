from pydantic import BaseSettings, Field


class SQLDBSettings(BaseSettings):
    sql_db_name:     str = Field(..., env='SQL_DB_NAME')
    sql_db_user:     str = Field(..., env='SQL_DB_USER')
    sql_db_password: str = Field(..., env='SQL_DB_PASSWORD')
    sql_db_host:     str = Field(..., env='SQL_DB_HOST')

    @property
    def sql_db_url(self):
        return 'postgresql://' \
               + self.sql_db_user \
               + ':' \
               + self.sql_db_password \
               + '@' \
               + self.sql_db_host \
               + '/' \
               + self.sql_db_name

class DocumentDBSettings(BaseSettings):
    mongo_db_name:      str = Field(..., env='MONGO_DB_NAME')
    mongo_db_user:      str = Field(..., env='MONGO_DB_USER')
    mongo_db_password:  str = Field(..., env='MONGO_DB_PASSWORD')
    mongo_db_host:      str = Field(..., env='MONGO_DB_HOST')

    @property
    def mongo_db_url(self):
        return 'mongodb://' \
            + self.mongo_db_user \
            + ':' \
            + self.mongo_db_password \
            + '@' \
            + self.mongo_db_host \
            + '/' \
            + self.mongo_db_name \
            + '?retryWrites=true&w=majority'

#export MONGODB_URL="mongodb+srv://<username>:<password>@<url>/<db>?retryWrites=true&w=majority"
sqldb_settings = SQLDBSettings()
mongodb_settings = DocumentDBSettings()
