from fastapi import FastAPI
from models import tasks
from sqlalchemy.orm import Session
from datetime import date
import databasemodel

databasemodel.Base.metadata.create_all(bind=engine)

app = FastAPI()
task_list=[
    tasks(task_id=1,task_name="wakeup at 5am",task_description="to maintain morning routine",is_completed=True,created_at="2026-08-22",priority="High",due_date="2026-08-22"),
    tasks(task_id=2,task_name="drink 5 lit of water",task_description="to keeping us hydrate",is_completed=True,created_at="2026-08-22",priority="High",due_date="2026-08-22"),
    tasks(task_id=3,task_name="no sugar",task_description="do not take sugar today",is_completed=False,created_at="2026-08-22",priority="Medium",due_date="2026-08-22"),
    tasks(task_id=4,task_name="study",task_description="to get good marks",is_completed=True,created_at="2026-08-22",priority="High",due_date="2026-08-22"),
    tasks(task_id=5,task_name="going to gym",task_description="to maintain our body physique",is_completed=False,created_at="2026-09-22",priority="High",due_date="2026-08-22")
    
]
 #to get all products
@app.get("/")
def get_all():
    return task_list

#to get a specific product
@app.get("/{task_id}")
def get_single_task(task_id:int):
    for task in task_list:
        if task.task_id == task_id:
            return task

#to post a new task
@app.post("/task")
def add_new_task(task:tasks):
    task_list.append(task)
    return task

#to uptade a task
@app.put("/task")
def update_task(task_id: int, task: tasks):
    for i in range(len(task_list)):
        if task_list[i].task_id == task_id:
            task_list[i] = task
            return task
        
# to delete a task
@app.delete("/task")
def delete_task(task_id: int):
    for task in task_list:
        if task.task_id == task_id:
            task_list.remove(task)