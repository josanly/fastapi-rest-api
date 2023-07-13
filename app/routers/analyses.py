from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy.orm import Session
from starlette import status

from app.databases import crud
from app.databases.document import get_document_db
from app.databases.relational import get_relationaldb
from app.models.analyses.schemas import CreateAnalysisRequest, AnalysisModel
from app.models.relational import Analysis
from app.routers.auth import get_current_user


router = APIRouter(
    prefix='/analyses',
    tags=['analyses']
)

user_dependency = Annotated[dict, Depends(get_current_user)]
relationaldb_dependency = Annotated[Session, Depends(get_relationaldb)]
documentdb_dependency = Annotated[AsyncIOMotorClient, Depends(get_document_db)]


@router.get('/', status_code=status.HTTP_200_OK)
async def list_analyses(db: relationaldb_dependency):
    return crud.list_analyses(db)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_analysis(user: user_dependency, db: relationaldb_dependency, create_analysis_request: CreateAnalysisRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    new_analysis = Analysis(
        title=create_analysis_request.title,
        description=create_analysis_request.description,
        priority=create_analysis_request.priority,
        owner_id=user.get('id')
    )
    await crud.create_or_update_analysis(db, new_analysis)


@router.get('/{analysis_id}', status_code=status.HTTP_200_OK)
async def get_analysis(user: user_dependency, db: relationaldb_dependency, analysis_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    analysis_entity = crud.get_analysis(db, analysis_id)
    if analysis_entity is not None:
        return analysis_entity
    raise HTTPException(status_code=404, detail='Analysis not found.')


@router.get('/details/{analysis_id}', status_code=status.HTTP_200_OK)
async def get_analysis_details(user: user_dependency,
                               db: relationaldb_dependency,
                               doc_db: documentdb_dependency,
                               analysis_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    analysis_entity, analysis_metadata = await crud.get_full_analysis_by_owner(db, doc_db, analysis_id, user.get('id'))
    if analysis_entity is not None:
        if analysis_metadata is not None:
            return analysis_metadata
        raise HTTPException(status_code=404, detail='Analysis Metadata not found.')
    raise HTTPException(status_code=404, detail='Analysis not found.')


@router.post("/details/{analysis_id}", status_code=status.HTTP_201_CREATED)
async def create_analysis(user: user_dependency,
                          db: relationaldb_dependency,
                          doc_db: documentdb_dependency,
                          analysis_metadata: AnalysisModel,
                          analysis_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    analysis_entity = crud.get_analysis_by_owner(db, analysis_id, user.get('id'))
    if analysis_entity is not None:
        await crud.create_or_update_analysis(db, analysis_entity, doc_db, jsonable_encoder(analysis_metadata))
    else:
        raise HTTPException(status_code=404, detail='Analysis not found.')



