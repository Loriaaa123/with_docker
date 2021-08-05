from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class FeedbackModel(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True)
    service_name = Column(String, nullable=False)
    tag = Column(String)
    created_at = Column(DateTime(timezone=True), default=datetime.now)
    data = Column(String, nullable=False)
