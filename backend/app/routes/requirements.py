from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.project import Project
from ..models.requirement import Requirement
from ..models.user import User
from ..routes.auth import get_current_user

router = APIRouter()


@router.get('/project/{project_id}')
def get_requirements(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = db.query(Project).filter(Project.id == project_id, Project.owner_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail='Project not found')
    return db.query(Requirement).filter(Requirement.project_id == project_id).all()


@router.get('/{requirement_id}')
def get_requirement(
    requirement_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    req = db.query(Requirement).filter(Requirement.id == requirement_id).first()
    if not req:
        raise HTTPException(status_code=404, detail='Requirement not found')

    project = db.query(Project).filter(Project.id == req.project_id, Project.owner_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail='Project not found')
    return req
