from sqlalchemy import Column, Integer, Text, String, Boolean, Date,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class user(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(500))

    tasks = relationship("Todo", back_populates="owner")

class Todo(Base):
    __tablename__ = "list"

    task_id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    task_name = Column(String(50))
    task_description = Column(Text)
    is_completed = Column(Boolean)
    created_at = Column(Date)
    priority = Column(String(10))
    due_date = Column(Date)
    owner_id = Column(Integer, ForeignKey("users.id"),nullable=True)
    owner = relationship("user",back_populates="tasks")










