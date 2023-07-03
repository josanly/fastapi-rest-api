from pydantic import BaseSettings, Field


class DBSettings(BaseSettings):
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


databases_settings = DBSettings()
