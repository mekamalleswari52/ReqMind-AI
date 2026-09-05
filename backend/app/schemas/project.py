from pydantic import BaseModel, ConfigDict
from typing import Optional


class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None


class ProjectOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    owner_id: int
    status: Optional[str] = "active"

    model_config = ConfigDict(from_attributes=True)
