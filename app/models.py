from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    status = Column(String, default="pending")  # Default status is "pending"
    result = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
