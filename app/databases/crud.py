from typing import Type, Tuple, Any, Coroutine

from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy.orm import Session

from app.models.analyses.schemas import AnalysisModel
from app.models.relational import User, Analysis


def create_user(db: Session, user: User) -> User:
    if user.id:
        return update_user(db, user)
    else:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user


def list_users(db: Session, skip: int = 0, limit: int = 100) -> list[Type[User]]:
    return db.query(User).offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_name(db: Session, user_name: str) -> User | None:
    return db.query(User).filter(User.username == user_name).first()


def update_user(db: Session, user: User) -> User | None:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int):
    db.delete(get_user(db, user_id))
    db.commit()


async def create_or_update_analysis(db: Session,
                              analysis: Analysis,
                              doc_db: AsyncIOMotorClient = None,
                              analysis_metadata: AnalysisModel = None) -> Analysis:
    if analysis.id:
        analysis = get_analysis(db, analysis.id)
    if analysis_metadata:
        new_analysis_metadata = await doc_db["analyses"].insert_one(analysis_metadata)
        await doc_db["analyses"].find_one({"_id": new_analysis_metadata.inserted_id})
        analysis.metadata_ref = new_analysis_metadata.inserted_id
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    return analysis


def list_analyses(db: Session, skip: int = 0, limit: int = 0) -> list[Type[Analysis]]:
    query = db.query(Analysis).offset(skip)
    if limit != 0:
        query = query.limit(limit)
    return query.all()


def list_analyses_by_owner(db: Session, owner_id: int, skip: int = 0, limit: int = 100) -> list[Type[Analysis]]:
    return db.query(Analysis) \
        .filter(Analysis.owner_id == owner_id) \
        .offset(skip) \
        .limit(limit) \
        .all()


def get_analysis(db: Session, analysis_id: int) -> Analysis | None:
    return db.query(Analysis).filter(Analysis.id == analysis_id).first()


def get_analysis_by_owner(db: Session, analysis_id: int, owner_id: int) -> Analysis | None:
    return db.query(Analysis) \
        .filter(Analysis.id == analysis_id) \
        .filter(Analysis.owner_id == owner_id) \
        .first()


async def get_full_analysis(db: Session,
                            doc_db: AsyncIOMotorClient,
                            analysis_id: int) -> tuple[Analysis | None, AnalysisModel | None]:
    return get_analysis(db, analysis_id), await get_analysis_metadata(db, doc_db, analysis_id)


async def get_full_analysis_by_owner(db: Session,
                                     doc_db: AsyncIOMotorClient,
                                     analysis_id: int,
                                     owner_id: int) -> tuple[Analysis, AnalysisModel | None] | tuple[None, None]:
    analysis_entity = get_analysis_by_owner(db, analysis_id, owner_id)
    if analysis_entity is not None:
        return analysis_entity, await get_analysis_metadata(db, doc_db, analysis_id)
    else:
        return None, None


async def get_analysis_metadata(db: Session,
                                doc_db: AsyncIOMotorClient,
                                analysis_id: int) -> AnalysisModel | None:
    analysis_entity = get_analysis(db, analysis_id)
    analysis_metadata = None
    if (analysis_entity is not None) and analysis_entity.metadata_ref:
        analysis_metadata = await doc_db["analyses"].find_one(
                {"_id": analysis_entity.metadata_ref}
        )
    return analysis_metadata
