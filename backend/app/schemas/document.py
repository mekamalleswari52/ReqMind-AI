from pydantic import BaseModel, ConfigDict
from typing import Optional


class DocumentOut(BaseModel):
    id: int
    project_id: int
    filename: str
    content: Optional[str]

    model_config = ConfigDict(from_attributes=True)
