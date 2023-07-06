from fastapi import Path
from pydantic import BaseModel


class CreateAnalysisRequest(BaseModel):
    title: str
    description: str
    priority: int = Path(gt=0, lt=6)
