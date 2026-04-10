from fastapi import FastAPI
from models import tasks
from datetime import date

app = FastAPI()

task_list=[
    tasks(task_id=1,task_name="wakeup at 5am",task_description="to maintain morning routine",is_completed=True,created_at="2026-08-22",priority="High",due_date="2026-08-22"),
    tasks(task_id=2,task_name="drink 5 lit of water",task_description="to keeping us hydrate",is_completed=True,created_at="2026-08-22",priority="High",due_date="2026-08-22"),
    tasks(task_id=3,task_name="no sugar",task_description="do not take sugar today",is_completed=False,created_at="2026-08-22",priority="Medium",due_date="2026-08-22"),
    tasks(task_id=1,task_name="study",task_description="to get good marks",is_completed=True,created_at="2026-08-22",priority="High",due_date="2026-08-22"),
    tasks(task_id=1,task_name="going to gym",task_description="to maintain our body physique",is_completed=False,created_at="2026-09-22",priority="High",due_date="2026-08-22")
    
]
 
@app.get("/")
def get_all():
    return task_list
