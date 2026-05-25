from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class Requirement(Base):
    __tablename__ = "requirements"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    module = Column(String(100))
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class TestCase(Base):
    __tablename__ = "test_cases"

    id = Column(Integer, primary_key=True, index=True)
    requirement_id = Column(Integer)
    test_case_id = Column(String(50))
    title = Column(String(255))
    priority = Column(String(50))
    precondition = Column(Text)
    steps = Column(Text)
    expected_result = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)