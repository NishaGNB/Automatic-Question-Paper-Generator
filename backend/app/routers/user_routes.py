from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..auth import get_db, get_current_user

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/me", response_model=schemas.UserBase)
def get_me(current_user: models.User = Depends(get_current_user)):
    return current_user


@router.get("/profile", response_model=schemas.FacultyProfileOut)
def get_profile(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    profile = db.query(models.FacultyProfile).filter(
        models.FacultyProfile.user_id == current_user.id
    ).first()
    return profile


@router.put("/profile", response_model=schemas.FacultyProfileOut)
def update_profile(
    profile_in: schemas.FacultyProfileUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    profile = db.query(models.FacultyProfile).filter(
        models.FacultyProfile.user_id == current_user.id
    ).first()
    if not profile:
        profile = models.FacultyProfile(user_id=current_user.id)
        db.add(profile)
        db.flush()
    profile.department = profile_in.department
    profile.designation = profile_in.designation
    db.commit()
    db.refresh(profile)
    return profile
