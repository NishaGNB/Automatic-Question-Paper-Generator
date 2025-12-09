from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, JSON, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base
import enum


class MaterialType(str, enum.Enum):
    reference = "reference"
    question_paper = "question_paper"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    profile = relationship("FacultyProfile", back_populates="user", uselist=False)
    question_papers = relationship("QuestionPaper", back_populates="user")


class FacultyProfile(Base):
    __tablename__ = "faculty_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    department = Column(String(100))
    designation = Column(String(100))
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="profile")


class SyllabusDoc(Base):
    __tablename__ = "syllabus_docs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    subject = Column(String(150), nullable=False)
    subject_code = Column(String(50), nullable=False)
    semester = Column(String(20), nullable=False)
    original_name = Column(String(255))
    file_path = Column(String(255))
    content_text = Column(Text)
    uploaded_at = Column(TIMESTAMP, server_default=func.now())


class ReferenceMaterial(Base):
    __tablename__ = "reference_materials"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    material_type = Column(Enum(MaterialType), default=MaterialType.reference)
    title = Column(String(255))
    original_name = Column(String(255))
    file_path = Column(String(255))
    content_text = Column(Text)
    uploaded_at = Column(TIMESTAMP, server_default=func.now())


class QuestionPaper(Base):
    __tablename__ = "question_papers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    subject = Column(String(150), nullable=False)
    subject_code = Column(String(50), nullable=False)
    semester = Column(String(20), nullable=False)
    total_marks = Column(Integer, nullable=False)
    set_number = Column(Integer, nullable=False)
    num_modules = Column(Integer, nullable=False)
    marks_distribution = Column(JSON)
    created_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User", back_populates="question_papers")
    questions = relationship("Question", back_populates="question_paper", cascade="all, delete-orphan")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question_paper_id = Column(Integer, ForeignKey("question_papers.id", ondelete="CASCADE"), nullable=False)
    module_number = Column(Integer, nullable=False)
    question_text = Column(Text, nullable=False)
    blooms_level = Column(String(50))
    marks = Column(Integer, nullable=False)
    question_hash = Column(String(64), index=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    question_paper = relationship("QuestionPaper", back_populates="questions")
