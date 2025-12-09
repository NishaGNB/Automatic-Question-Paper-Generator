from typing import List, Optional
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserBase(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        # Pydantic v2: use `from_attributes` instead of `orm_mode`.
        from_attributes = True


class FacultyProfileBase(BaseModel):
    department: Optional[str] = None
    designation: Optional[str] = None


class FacultyProfileUpdate(FacultyProfileBase):
    pass


class FacultyProfileOut(FacultyProfileBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


class ModuleInput(BaseModel):
    module_number: int
    title: str
    topics: str
    num_questions: int
    marks: int


class GeneratePaperRequest(BaseModel):
    semester: str
    subject: str
    subject_code: str
    total_marks: int
    modules: List[ModuleInput]
    marks_distribution: Optional[dict] = None
    syllabus_doc_id: int
    reference_material_ids: List[int]
    reference_question_material_ids: List[int] = []


class QuestionOut(BaseModel):
    id: int
    module_number: int
    question_text: str
    blooms_level: Optional[str]
    marks: int

    class Config:
        from_attributes = True


class QuestionPaperOut(BaseModel):
    id: int
    set_number: int
    subject: str
    subject_code: str
    semester: str
    total_marks: int
    num_modules: int
    questions: List[QuestionOut]

    class Config:
        from_attributes = True
