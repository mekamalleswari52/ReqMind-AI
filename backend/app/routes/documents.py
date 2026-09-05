from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Form
from sqlalchemy.orm import Session
import os

from ..database import get_db
from ..models.document import Document
from ..models.project import Project
from ..models.user import User
from ..routes.auth import get_current_user
from ..schemas.document import DocumentOut
from ..config import MAX_UPLOAD_SIZE

router = APIRouter()

UPLOAD_DIR = os.path.abspath(os.path.join(os.getcwd(), "uploads"))
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload", response_model=DocumentOut)
def upload_document(
    file: UploadFile = File(...),
    project_id: int = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = db.query(Project).filter(Project.id == project_id, Project.owner_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    contents = file.file.read()
    if len(contents) == 0:
        raise HTTPException(status_code=400, detail="Empty file")
    if len(contents) > MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=400, detail="File too large")

    safe_name = os.path.basename(file.filename)
    path = os.path.join(UPLOAD_DIR, safe_name)
    with open(path, "wb") as f:
        f.write(contents)

    doc = Document(project_id=project_id, filename=safe_name, content=None)
    db.add(doc)
    db.commit()
    db.refresh(doc)

    from ..services.document_service import extract_text

    text = extract_text(path, safe_name)
    if text:
        doc.content = text
        db.commit()
        db.refresh(doc)
    return doc
