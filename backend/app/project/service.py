from typing import List, Optional
from fastapi import HTTPException, status
from app.project.repo import ProjectRepository
from app.project.schema import ProjectCreate, ProjectUpdate, ProjectResponse

class ProjectService:
    def __init__(self, repository: ProjectRepository):
        self.repository = repository

    def create_project(self, project_data: ProjectCreate) -> ProjectResponse:
        """Create a new project with business logic validation"""
        # Add any business logic here (e.g., name uniqueness check)
        project = self.repository.create(project_data)
        return ProjectResponse.model_validate(project)

    def get_project(self, project_id: int) -> ProjectResponse:
        """Get a single project by ID"""
        project = self.repository.get_by_id(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with id {project_id} not found"
            )
        return ProjectResponse.model_validate(project)

    def get_all_projects(
        self, 
        skip: int = 0, 
        limit: int = 100, 
        active_only: bool = False
    ) -> List[ProjectResponse]:
        """Get all projects with optional filtering"""
        if active_only:
            projects = self.repository.get_active(skip, limit)
        else:
            projects = self.repository.get_all(skip, limit)
        
        return [ProjectResponse.model_validate(p) for p in projects]

    def update_project(
        self, 
        project_id: int, 
        project_data: ProjectUpdate
    ) -> ProjectResponse:
        """Update a project"""
        project = self.repository.update(project_id, project_data)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with id {project_id} not found"
            )
        return ProjectResponse.model_validate(project)

    def delete_project(self, project_id: int, soft: bool = False) -> dict:
        """Delete a project (soft or hard delete)"""
        if soft:
            project = self.repository.soft_delete(project_id)
            if not project:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Project with id {project_id} not found"
                )
            return {"message": "Project deactivated successfully"}
        else:
            deleted = self.repository.delete(project_id)
            if not deleted:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Project with id {project_id} not found"
                )
            return {"message": "Project deleted successfully"}