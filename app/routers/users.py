from typing import Annotated

from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from app.databases.relational import get_relationaldb
from .auth import get_current_user
from ..databases import crud
from ..models.users.schemas import UserVerification


router = APIRouter(
    prefix='/users',
    tags=['users']
)

relationaldb_dependency = Annotated[Session, Depends(get_relationaldb)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: relationaldb_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')
    return crud.get_user(db, user.get('id'))


@router.put('/password', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: relationaldb_dependency, user_verif: UserVerification):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')
    user_entity = crud.get_user(db, user.get('id'))
    if not bcrypt_context.verify(user_verif.password, user_entity.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Error on password change')
    user_entity.hashed_password = bcrypt_context.hash(user_verif.new_password)
    crud.update_user(db, user_entity)
