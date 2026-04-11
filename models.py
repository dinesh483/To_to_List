from pydantic import BaseModel
from datetime import date
from typing import Optional

class tasks(BaseModel):
   task_id: Optional[int] = None
   task_name: str
   task_description: str
   is_completed: bool
   created_at: date
   priority: str
   due_date: date