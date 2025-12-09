import os
from fastapi import APIRouter, UploadFile, File, Depends, Form
from sqlalchemy.orm import Session

from ..auth import get_db, get_current_user
from .. import models
from ..config import settings
from ..models import MaterialType

router = APIRouter(prefix="/files", tags=["files"])

os.makedirs(settings.FILE_UPLOAD_DIR, exist_ok=True)


def read_file_text(file_path: str) -> str:
    # For demo: only handle .txt; extend to PDF/docx as needed.
    if file_path.lower().endswith(".txt"):
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    return ""


@router.post("/upload-syllabus")
async def upload_syllabus(
    semester: str = Form(...),
    subject: str = Form(...),
    subject_code: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    save_path = os.path.join(settings.FILE_UPLOAD_DIR, file.filename)
    with open(save_path, "wb") as f:
        f.write(await file.read())

    content_text = read_file_text(save_path)
    doc = models.SyllabusDoc(
        user_id=current_user.id,
        subject=subject,
        subject_code=subject_code,
        semester=semester,
        original_name=file.filename,
        file_path=save_path,
        content_text=content_text,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return {"id": doc.id, "message": "Syllabus uploaded"}


@router.post("/upload-reference")
async def upload_reference(
    title: str = Form(...),
    material_type: MaterialType = Form(MaterialType.reference),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    save_path = os.path.join(settings.FILE_UPLOAD_DIR, file.filename)
    with open(save_path, "wb") as f:
        f.write(await file.read())

    content_text = read_file_text(save_path)
    ref = models.ReferenceMaterial(
        user_id=current_user.id,
        title=title,
        original_name=file.filename,
        file_path=save_path,
        content_text=content_text,
        material_type=material_type,
    )
    db.add(ref)
    db.commit()
    db.refresh(ref)
    return {"id": ref.id, "message": "Reference uploaded"}
