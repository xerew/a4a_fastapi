from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.config import Base

class Pipeline(Base):
    __tablename__ = "pipelines"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)  # From cookie
    name = Column(String(255), nullable=False)
    data = Column(Text, nullable=False)  # Will store JSON string
