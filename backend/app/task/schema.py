from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1)
    description: Optional[str] = None
    status: Optional[str] = "not_started"
    priority: Optional[str] = "medium"
    due_date: Optional[datetime] = None
    position: Optional[str] = None

class TaskCreate(TaskBase):
    project_id: UUID
    assigned_to: Optional[UUID] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    assigned_to: Optional[UUID] = None
    due_date: Optional[datetime] = None
    position: Optional[str] = None

class TaskResponse(TaskBase):
    id: UUID
    project_id: UUID
    assigned_to: Optional[UUID] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True