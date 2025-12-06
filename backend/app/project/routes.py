from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
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


def get_project_by_id(db: Session, project_id: int) -> Optional[Project]:
    """Get a project by ID from the database"""
    return db.query(Project).filter(Project.id == project_id).first()


def get_all_projects_from_db(db: Session, skip: int = 0, limit: int = 100, active_only: bool = False) -> List[Project]:
    """Get all projects from the database with optional filtering"""
    query = db.query(Project)
    if active_only:
        query = query.filter(Project.is_active == True)
    return query.offset(skip).limit(limit).all()


def update_project_in_db(db: Session, project_id: int, project_data: ProjectUpdate) -> Optional[Project]:
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


def delete_project_from_db(db: Session, project_id: int) -> bool:
    """Delete a project from the database (hard delete)"""
    db_project = get_project_by_id(db, project_id)
    if not db_project:
        return False
    
    db.delete(db_project)
    db.commit()
    return True


def soft_delete_project_in_db(db: Session, project_id: int) -> Optional[Project]:
    """Soft delete a project by setting is_active to False"""
    db_project = get_project_by_id(db, project_id)
    if not db_project:
        return None
    
    db_project.is_active = False
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
    - **name**: Project name (required)
    - **description**: Project description (optional)
    - **status**: Project status (default: active)
    - **is_active**: Whether the project is active (default: true)
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
    active_only: bool = Query(False, description="Filter only active projects"),
    db: Session = Depends(get_db)
):
    """
    Retrieve all projects with pagination and optional filtering.
    """
    projects = get_all_projects_from_db(db, skip=skip, limit=limit, active_only=active_only)
    return [ProjectResponse.model_validate(p) for p in projects]


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Get a project by ID"
)
def get_project(
    project_id: int,
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
    project_id: int,
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
    project_id: int,
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
    project_id: int,
    soft: bool = Query(False, description="Use soft delete (deactivate) instead of hard delete"),
    db: Session = Depends(get_db)
):
    """
    Delete a project. Use soft=true for soft delete (sets is_active to false).
    """
    if soft:
        project = soft_delete_project_in_db(db, project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with id {project_id} not found"
            )
        return {"message": "Project deactivated successfully"}
    else:
        deleted = delete_project_from_db(db, project_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with id {project_id} not found"
            )
        return {"message": "Project deleted successfully"}
