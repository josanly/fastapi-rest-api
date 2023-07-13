import os
import pytest
from sqlalchemy.dialects import sqlite


@pytest.fixture
def override_sqldb_settings():
    import app.tests.helpers

    yield app.tests.helpers.override_sqldb_settings


def setup_env():
    os.environ["SECRETS_DIR"] = './resources'

    os.environ["SQL_DB_USER"] = ''
    os.environ["SQL_DB_NAME"] = 'test'
    os.environ["SQL_DB_HOST"] = ''
    os.environ["SQL_DB_PASSWORD"] = ''
    # os.environ["SQL_DB_URL"] = 'sqlite:///./testing.db'
    os.environ["SQL_DB_URL"] = 'sqlite://'

    os.environ["MONGO_DB_NAME"] = 'docdb'
    os.environ["MONGO_DB_USER"] = 'restapp'
    os.environ["MONGO_DB_PASSWORD"] = 'test'
    os.environ["MONGO_DB_HOST"] = 'mongodb:27017'
    # os.environ[""] = ''
    # os.environ[""] = ''
