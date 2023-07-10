from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy.orm import Session
from starlette import status

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
    return db.query(Analysis).all()


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
    db.add(new_analysis)
    db.commit()


@router.get('/{analysis_id}', status_code=status.HTTP_200_OK)
async def get_analysis(user: user_dependency, db: relationaldb_dependency, analysis_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    analysis_model = db.query(Analysis) \
                       .filter(Analysis.id == analysis_id) \
                       .filter(Analysis.owner_id == user.get('id')) \
                       .first()
    if analysis_model is not None:
        return analysis_model
    raise HTTPException(status_code=404, detail='Analysis not found.')



@router.get('/details/{analysis_id}', status_code=status.HTTP_200_OK)
async def get_analysis_details(user: user_dependency,
                               db: relationaldb_dependency,
                               doc_db: documentdb_dependency,
                               analysis_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    analysis_model = db.query(Analysis) \
                       .filter(Analysis.id == analysis_id) \
                       .filter(Analysis.owner_id == user.get('id')) \
                       .first()
    if analysis_model is not None:
        analysis_metadata = await doc_db["analyses"].find_one(
            {"_id": analysis_model.metadata_ref}
        )
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
    analysis_model = db.query(Analysis) \
                        .filter(Analysis.id == analysis_id) \
                        .filter(Analysis.owner_id == user.get('id')) \
                        .first()
    analysis_metadata = jsonable_encoder(analysis_metadata)
    new_analysis_metadata = await doc_db["analyses"].insert_one(analysis_metadata)
    await doc_db["analyses"].find_one({"_id": new_analysis_metadata.inserted_id})
    analysis_model.metadata_ref = new_analysis_metadata.inserted_id
    db.add(analysis_model)
    db.commit()


