from sqlalchemy import Column, Integer, Text, String, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Todo(Base):
    __tablename__ = "list"

    task_id = Column(Integer, primary_key=True, index=True)
    task_name = Column(String(50))
    task_description = Column(Text)
    is_completed = Column(Boolean)
    created_at = Column(Date)
    priority = Column(String(10))
    due_date = Column(Date)










