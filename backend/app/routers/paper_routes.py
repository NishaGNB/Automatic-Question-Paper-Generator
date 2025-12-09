from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..auth import get_db, get_current_user
from .. import models, schemas
from ..llm_service import generate_question_sets
from ..utils import question_hash

router = APIRouter(prefix="/papers", tags=["papers"])


@router.post("/generate", response_model=List[schemas.QuestionPaperOut])
def generate_papers(
    payload: schemas.GeneratePaperRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    syllabus = db.query(models.SyllabusDoc).filter(
        models.SyllabusDoc.id == payload.syllabus_doc_id,
        models.SyllabusDoc.user_id == current_user.id,
    ).first()
    if not syllabus:
        raise HTTPException(status_code=404, detail="Syllabus not found")

    base_query = db.query(models.ReferenceMaterial).filter(
        models.ReferenceMaterial.user_id == current_user.id
    )

    refs = base_query.filter(
        models.ReferenceMaterial.id.in_(payload.reference_material_ids),
        models.ReferenceMaterial.material_type == models.MaterialType.reference,
    ).all()

    ref_qps = []
    if payload.reference_question_material_ids:
        ref_qps = base_query.filter(
            models.ReferenceMaterial.id.in_(payload.reference_question_material_ids),
            models.ReferenceMaterial.material_type == models.MaterialType.question_paper,
        ).all()

    if not refs and not ref_qps:
        raise HTTPException(status_code=404, detail="No reference materials found")

    reference_text = (syllabus.content_text or "") + "\n\n"
    reference_text += "\n\n".join([r.content_text or "" for r in refs + ref_qps])

    old_qs = (
        db.query(models.Question)
        .join(models.QuestionPaper)
        .filter(
            models.QuestionPaper.user_id == current_user.id,
            models.QuestionPaper.subject == payload.subject,
            models.QuestionPaper.subject_code == payload.subject_code,
            models.QuestionPaper.semester == payload.semester,
        )
        .all()
    )
    existing_texts = [q.question_text for q in old_qs]

    modules_data = [
        {
            "module_number": m.module_number,
            "title": m.title,
            "topics": m.topics,
            "num_questions": m.num_questions,
            "marks": m.marks,
        }
        for m in payload.modules
    ]

    llm_result = generate_question_sets(
        modules=modules_data,
        reference_text=reference_text,
        existing_questions=existing_texts,
        num_sets=3,
    )

    papers_out = []
    used_hashes_in_batch = set()

    for set_obj in llm_result.get("sets", []):
        set_number = set_obj.get("set_number", 0)
        qp = models.QuestionPaper(
            user_id=current_user.id,
            subject=payload.subject,
            subject_code=payload.subject_code,
            semester=payload.semester,
            total_marks=payload.total_marks,
            set_number=set_number,
            num_modules=len(payload.modules),
            marks_distribution=payload.marks_distribution,
        )
        db.add(qp)
        db.flush()

        for module in set_obj.get("modules", []):
            module_number = module.get("module_number")
            for q in module.get("questions", []):
                q_text = (q.get("text") or "").strip()
                if not q_text:
                    continue
                q_hash = question_hash(q_text)

                if q_hash in used_hashes_in_batch:
                    continue
                existing_q = (
                    db.query(models.Question)
                    .join(models.QuestionPaper)
                    .filter(
                        models.Question.question_hash == q_hash,
                        models.QuestionPaper.user_id == current_user.id,
                    )
                    .first()
                )
                if existing_q:
                    continue

                question = models.Question(
                    question_paper_id=qp.id,
                    module_number=module_number,
                    question_text=q_text,
                    marks=int(q.get("marks", 0)),
                    blooms_level=q.get("blooms_level"),
                    question_hash=q_hash,
                )
                db.add(question)
                used_hashes_in_batch.add(q_hash)

        db.commit()
        db.refresh(qp)
        papers_out.append(qp)

    return papers_out


@router.get("/", response_model=List[schemas.QuestionPaperOut])
def list_papers(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    papers = (
        db.query(models.QuestionPaper)
        .filter(models.QuestionPaper.user_id == current_user.id)
        .order_by(models.QuestionPaper.created_at.desc())
        .all()
    )
    return papers


@router.get("/{paper_id}", response_model=schemas.QuestionPaperOut)
def get_paper(
    paper_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    qp = (
        db.query(models.QuestionPaper)
        .filter(
            models.QuestionPaper.id == paper_id,
            models.QuestionPaper.user_id == current_user.id,
        )
        .first()
    )
    if not qp:
        raise HTTPException(status_code=404, detail="Question paper not found")
    return qp
