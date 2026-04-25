from fastapi import FastAPI,Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from models import tasks
from sqlalchemy.orm import Session
from datetime import date
from database import SessionLocal,engine
import databasemodel
from passlib.context import CryptContext

databasemodel.Base.metadata.create_all(bind=engine)

SECURITY_KEY = "TODOLIST"
ALGORITHM = "HS256"
TOKEN_EXPIRE = 30


app = FastAPI()

# CORS for frontend dev server
app.add_middleware(
     CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
task_list=[
    tasks(task_id=1,task_name="wakeup at 5am",task_description="to maintain morning routine",is_completed=True,created_at="2026-08-22",priority="High",due_date="2026-08-22"),
    tasks(task_id=2,task_name="drink 5 lit of water",task_description="to keeping us hydrate",is_completed=True,created_at="2026-08-22",priority="High",due_date="2026-08-22"),
    tasks(task_id=3,task_name="no sugar",task_description="do not take sugar today",is_completed=False,created_at="2026-08-22",priority="Medium",due_date="2026-08-22"),
    tasks(task_id=4,task_name="study",task_description="to get good marks",is_completed=True,created_at="2026-08-22",priority="High",due_date="2026-08-22"),
    tasks(task_id=5,task_name="going to gym",task_description="to maintain our body physique",is_completed=False,created_at="2026-09-22",priority="High",due_date="2026-08-22")
    
]
def init_db():
    db = SessionLocal()

    existing_count = db.query(databasemodel.Todo).count()

    if existing_count == 0:
        for task in task_list:
            db.add(databasemodel.Todo(**task.model_dump()))
        db.commit()
        print("Database initialized with sample products.")
        
    db.close()

init_db()    

 #to get all products
@app.get("/task")
def get_all(db:Session=Depends(get_db)):
    task=db.query(databasemodel.Todo).all()
    return task

#to get a specific product
@app.get("/task/{task_id}")
def get_single_task(task_id:int,db:Session=Depends(get_db)):
   task = db.query(databasemodel.Todo).filter(databasemodel.Todo.task_id == task_id).first()
   if task:
       return task
   else:
       return {"error":"task not found"}
   
#to post a new task
@app.post("/task")
def create_task(task: tasks, db: Session = Depends(get_db)):
    task_data = task.model_dump(exclude={"task_id"})
    db.add(databasemodel.Todo(**task_data))
    db.commit()
    return {"message": "Task created successfully"}

#to uptade a task
@app.put("/task/{task_id}")
def update_task(task_id: int, task: tasks, db: Session = Depends(get_db)):
    db_task = db.query(databasemodel.Todo).filter(databasemodel.Todo.task_id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="task not found")
    db_task.task_name = task.task_name
    db_task.task_description = task.task_description
    db_task.is_completed = task.is_completed
    db_task.created_at = task.created_at
    db_task.priority = task.priority
    db_task.due_date = task.due_date
    db.commit()
    db.refresh(db_task)
    return {"message": "Product updated successfully", "task": db_task}
        
# to delete a task
@app.delete("/task/{task_id}")
def delete_task(task_id: int,db: Session = Depends(get_db)):
    db_task = db.query(databasemodel.Todo).filter(databasemodel.Todo.task_id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="task not found")
    db.delete(db_task)
    db.commit()
    return {"message": "task deleted successfully"}