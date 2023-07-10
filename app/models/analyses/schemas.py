from typing import Optional

from bson import ObjectId
from fastapi import Path
from pydantic import BaseModel, EmailStr, Field

from app.models import PyObjectId


class CreateAnalysisRequest(BaseModel):
    title: str
    description: str
    priority: int = Path(gt=0, lt=6)


class UpdateAnalysisModel(BaseModel):
    name: Optional[str]
    client_contact: Optional[EmailStr]
    start: Optional[int]
    end: Optional[int]
    status: str = Field(...)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class AnalysisModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    client_contact:  EmailStr = Field(...)
    start: int = Field(...)
    end: int = Field(...)
    status: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        #schema_extra = {
        #    "example": {
        #        "name": "Jane Doe",
        #        "email": "jdoe@example.com",
        #        "course": "Experiments, Science, and Fashion in Nanophotonics",
        #        "gpa": "3.0",
        #    }
        #}
