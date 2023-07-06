from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr
from pydantic.fields import Optional


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


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


class UpdateAnalysisModel(BaseModel):
    name: Optional[str]
    client_contact: Optional[EmailStr]
    start: Optional[int]
    end: Optional[int]
    status: str = Field(...)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
