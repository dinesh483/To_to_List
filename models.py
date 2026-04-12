from pydantic import BaseModel
from datetime import date
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class tasks(BaseModel):
   task_id: Optional[int] = None
   task_name: str
   task_description: str
   is_completed: bool
   created_at: date
   priority: str
   due_date: date
   owner_id: Optional[int] = None