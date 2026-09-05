from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.analysis import Analysis
from ..models.document import Document
from ..models.project import Project
from ..models.requirement import Requirement
from ..models.user import User
from ..routes.auth import get_current_user
from ..services.ai_service import AIService

router = APIRouter()


@router.post('/document/{document_id}')
def analyze_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail='Document not found')

    project = db.query(Project).filter(Project.id == doc.project_id, Project.owner_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=403, detail='You do not have access to this project')

    texts = []
    if doc.content:
        for line in doc.content.splitlines():
            line = line.strip()
            if not line:
                continue
            if line.upper().startswith('REQ') or line.lower().startswith('the '):
                texts.append(line)

    req_objs = []
    for i, text in enumerate(texts, start=1):
        requirement = Requirement(
            requirement_id=f"REQ-{document_id}-{i}",
            project_id=doc.project_id,
            document_id=doc.id,
            text=text,
        )
        db.add(requirement)
        db.commit()
        db.refresh(requirement)
        req_objs.append(requirement)

    ai = AIService()
    analyses = ai.analyze_requirements([item.text for item in req_objs])

    analysis = Analysis(
        project_id=doc.project_id,
        document_id=doc.id,
        summary='Auto analysis',
        results=analyses,
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    return {"analysis_id": analysis.id, "requirements": [item.id for item in req_objs]}
