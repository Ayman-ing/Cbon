from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from app.core.database import get_db
from app.project.model import Project
from app.project.schema import ProjectCreate, ProjectUpdate, ProjectResponse

router = APIRouter(prefix="/projects", tags=["Projects"])


# Database operations
def create_project_in_db(db: Session, project_data: ProjectCreate) -> Project:
    """Create a new project in the database"""
    db_project = Project(**project_data.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def get_project_by_id(db: Session, project_id: UUID) -> Optional[Project]:
    """Get a project by ID from the database"""
    return db.query(Project).filter(Project.id == project_id).first()


def get_all_projects_from_db(db: Session, skip: int = 0, limit: int = 100, status_filter: Optional[str] = None) -> List[Project]:
    """Get all projects from the database with optional filtering"""
    query = db.query(Project)
    if status_filter:
        query = query.filter(Project.status == status_filter)
    return query.offset(skip).limit(limit).all()


def update_project_in_db(db: Session, project_id: UUID, project_data: ProjectUpdate) -> Optional[Project]:
    """Update a project in the database"""
    db_project = get_project_by_id(db, project_id)
    if not db_project:
        return None
    
    update_data = project_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_project, field, value)
    
    db.commit()
    db.refresh(db_project)
    return db_project


def delete_project_from_db(db: Session, project_id: UUID) -> bool:
    """Delete a project from the database (hard delete)"""
    db_project = get_project_by_id(db, project_id)
    if not db_project:
        return False
    
    db.delete(db_project)
    db.commit()
    return True


def soft_delete_project_in_db(db: Session, project_id: UUID) -> Optional[Project]:
    """Soft delete a project by setting status to 'archived'"""
    db_project = get_project_by_id(db, project_id)
    if not db_project:
        return None
    
    db_project.status = 'archived'
    db.commit()
    db.refresh(db_project)
    return db_project


# API Routes
@router.post(
    "/",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new project"
)
def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new project with the following information:
    - **title**: Project title (required)
    - **description**: Project description (optional)
    - **status**: Project status (default: active)
    - **owner_id**: Project owner UUID (optional)
    """
    project = create_project_in_db(db, project_data)
    return ProjectResponse.model_validate(project)


@router.get(
    "/",
    response_model=List[ProjectResponse],
    summary="Get all projects"
)
def get_all_projects(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return"),
    status_filter: Optional[str] = Query(None, description="Filter projects by status"),
    db: Session = Depends(get_db)
):
    """
    Retrieve all projects with pagination and optional filtering.
    """
    projects = get_all_projects_from_db(db, skip=skip, limit=limit, status_filter=status_filter)
    return [ProjectResponse.model_validate(p) for p in projects]


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Get a project by ID"
)
def get_project(
    project_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific project by its ID.
    """
    project = get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found"
        )
    return ProjectResponse.model_validate(project)


@router.put(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Update a project"
)
def update_project(
    project_id: UUID,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a project's information. Only provided fields will be updated.
    """
    project = update_project_in_db(db, project_id, project_data)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found"
        )
    return ProjectResponse.model_validate(project)


@router.patch(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Partially update a project"
)
def patch_project(
    project_id: UUID,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db)
):
    """
    Partially update a project. Same as PUT but semantically indicates partial update.
    """
    project = update_project_in_db(db, project_id, project_data)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found"
        )
    return ProjectResponse.model_validate(project)


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a project"
)
def delete_project(
    project_id: UUID,
    soft: bool = Query(False, description="Use soft delete (archive) instead of hard delete"),
    db: Session = Depends(get_db)
):
    """
    Delete a project. Use soft=true for soft delete (sets status to 'archived').
    """
    if soft:
        project = soft_delete_project_in_db(db, project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with id {project_id} not found"
            )
        return {"message": "Project archived successfully"}
    else:
        deleted = delete_project_from_db(db, project_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with id {project_id} not found"
            )
        return {"message": "Project deleted successfully"}
