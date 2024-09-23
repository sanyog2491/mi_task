from sqlalchemy import Column, Integer, String
from app.core.config import Base

class Video(Base):
    __tablename__ = 'videos'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    size = Column(Integer)
    path = Column(String)
    converted = Column(String, default="Pending")  