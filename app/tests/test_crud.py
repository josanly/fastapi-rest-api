from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

from app.tests import setup_env


# fix definition of required env vars
setup_env()

from app.databases.relational import Base
from app.databases import crud
from app.models.relational import User
from app.routers.auth import bcrypt_context


SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

test_db = TestingSessionLocal()

# ref data to test
username = 'foo'
first_name = 'first_name'
last_name = 'last_name'
role = 'role'
password = 'secret_password'
hashed_password = bcrypt_context.hash(password)
email = 'foo@bar.com'


# def setup_module(module):
#     """ setup any state specific to the execution of the given module."""
#
#
# def teardown_module(module):
#     """ teardown any state that was previously setup with a setup_module
#     method."""

def user_entity_assertion(user):
    assert user.id == 1
    assert user.email == email
    assert user.username == username
    assert user.first_name == first_name
    assert user.last_name == last_name
    assert user.role == role
    assert user.hashed_password == hashed_password
    assert bcrypt_context.verify(password, user.hashed_password)


def test_create_user():
    user = crud.create_user(test_db,
                            User(
                                    email=email,
                                    username=username,
                                    first_name=first_name,
                                    last_name=last_name,
                                    role=role,
                                    hashed_password=hashed_password,
                                    is_active=True))
    user_entity_assertion(user)


def test_get_user():
    user = crud.get_user(test_db, 1)
    user_entity_assertion(user)


def test_list_users():
    users = crud.list_users(test_db)
    assert len(users) == 1
    user_entity_assertion(users[0])


def test_update_user():
    user = crud.get_user(test_db, 1)
    user_entity_assertion(user)
    new_name = 'other'
    user.username = new_name
    new_password = 'new_password'
    user.hashed_password = new_password
    user = crud.update_user(test_db, user)
    assert user.username == new_name
    assert user.hashed_password == new_password


def test_delete_user():
    crud.delete_user(test_db, 1)
    user = crud.get_user(test_db, 1)
    assert user is None
    users = crud.list_users(test_db)
    assert len(users) == 0
