from pydantic import BaseModel
from typing import List, Dict

class TimetableEntryBase(BaseModel):
    period_index: int
    class_name: str
    subject: str

class TimetableCreate(BaseModel):
    name: str
    entries: Dict[str, List[str]] # Class -> List of Subjects
    periods: int

class TimetableResponse(BaseModel):
    id: int
    name: str
    created_at: str
    entries: List[TimetableEntryBase]

    class Config:
        from_attributes = True

class GenerateRequest(BaseModel):
    periods: int
    classes: Dict[str, List[str]] # Class -> List of Subjects to process
