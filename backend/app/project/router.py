from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.project.repo import ProjectRepository
from app.project.service import ProjectService
from app.project.schema import ProjectCreate, ProjectUpdate, ProjectResponse

router = APIRouter(prefix="/projects", tags=["Projects"])

# Dependency injection for service layer
def get_project_service(db: Session = Depends(get_db)) -> ProjectService:
    repository = ProjectRepository(db)
    return ProjectService(repository)

@router.post(
    "/",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new project"
)
def create_project(
    project_data: ProjectCreate,
    service: ProjectService = Depends(get_project_service)
):
    """
    Create a new project with the following information:
    - **name**: Project name (required)
    - **description**: Project description (optional)
    - **status**: Project status (default: active)
    - **is_active**: Whether the project is active (default: true)
    """
    return service.create_project(project_data)

@router.get(
    "/",
    response_model=List[ProjectResponse],
    summary="Get all projects"
)
def get_all_projects(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return"),
    active_only: bool = Query(False, description="Filter only active projects"),
    service: ProjectService = Depends(get_project_service)
):
    """
    Retrieve all projects with pagination and optional filtering.
    """
    return service.get_all_projects(skip=skip, limit=limit, active_only=active_only)

@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Get a project by ID"
)
def get_project(
    project_id: int,
    service: ProjectService = Depends(get_project_service)
):
    """
    Retrieve a specific project by its ID.
    """
    return service.get_project(project_id)

@router.put(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Update a project"
)
def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    service: ProjectService = Depends(get_project_service)
):
    """
    Update a project's information. Only provided fields will be updated.
    """
    return service.update_project(project_id, project_data)

@router.patch(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Partially update a project"
)
def patch_project(
    project_id: int,
    project_data: ProjectUpdate,
    service: ProjectService = Depends(get_project_service)
):
    """
    Partially update a project. Same as PUT but semantically indicates partial update.
    """
    return service.update_project(project_id, project_data)

@router.delete(
    "/{project_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a project"
)
def delete_project(
    project_id: int,
    soft: bool = Query(False, description="Use soft delete (deactivate) instead of hard delete"),
    service: ProjectService = Depends(get_project_service)
):
    """
    Delete a project. Use soft=true for soft delete (sets is_active to false).
    """
    return service.delete_project(project_id, soft=soft)