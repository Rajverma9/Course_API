from sqlmodel import SQLModel, Field 
from typing import Optional

class Course(SQLModel, table=True):
    Course_id: Optional[int] = Field(default=None, primary_key=True)
    Course_Name: str
    duration_weak: int
    Course_fee: int
    is_active: bool=True



