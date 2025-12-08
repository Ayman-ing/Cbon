from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date
from uuid import UUID

# Project Schemas
class ProjectBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[str] = "active"
    start_date: Optional[date] = None
    due_date: Optional[date] = None

class ProjectCreate(ProjectBase):
    owner_id: Optional[UUID] = None

class ProjectUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[str] = None
    start_date: Optional[date] = None
    due_date: Optional[date] = None
    owner_id: Optional[UUID] = None

class ProjectResponse(ProjectBase):
    id: UUID
    owner_id: Optional[UUID] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Project Member Schemas
class ProjectMemberBase(BaseModel):
    user_id: UUID
    project_id: UUID
    role: Optional[str] = None

class ProjectMemberCreate(ProjectMemberBase):
    pass

class ProjectMemberResponse(ProjectMemberBase):
    joined_at: datetime

    class Config:
        from_attributes = True

