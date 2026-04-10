from pydantic import BaseModel
from datetime import date

class tasks(BaseModel):
   task_id:int
   task_name:str
   task_description:str
   is_completed:bool
   created_at:date
   priority:str
   due_date:date