from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class TestCase(Base):
    __tablename__ = "test_cases"
    id = Column(Integer, primary_key=True, index=True)
    requirement_id = Column(Integer, ForeignKey("requirements.id"), nullable=False)
    title = Column(String, nullable=False)
    scenario = Column(Text)
    steps = Column(Text)
    expected = Column(Text)
    priority = Column(String, default="medium")
    test_type = Column(String, default="functional")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    requirement = relationship("Requirement")
