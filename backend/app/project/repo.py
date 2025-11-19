from sqlalchemy.orm import Session
from typing import List, Optional
from app.project.model import Project
from app.project.schema import ProjectCreate, ProjectUpdate

class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, project_data: ProjectCreate) -> Project:
        """Create a new project"""
        db_project = Project(**project_data.model_dump())
        self.db.add(db_project)
        self.db.commit()
        self.db.refresh(db_project)
        return db_project

    def get_by_id(self, project_id: int) -> Optional[Project]:
        """Get a project by ID"""
        return self.db.query(Project).filter(Project.id == project_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Project]:
        """Get all projects with pagination"""
        return self.db.query(Project).offset(skip).limit(limit).all()

    def get_active(self, skip: int = 0, limit: int = 100) -> List[Project]:
        """Get only active projects"""
        return self.db.query(Project).filter(
            Project.is_active == True
        ).offset(skip).limit(limit).all()

    def update(self, project_id: int, project_data: ProjectUpdate) -> Optional[Project]:
        """Update a project"""
        db_project = self.get_by_id(project_id)
        if not db_project:
            return None
        
        update_data = project_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_project, field, value)
        
        self.db.commit()
        self.db.refresh(db_project)
        return db_project

    def delete(self, project_id: int) -> bool:
        """Delete a project (hard delete)"""
        db_project = self.get_by_id(project_id)
        if not db_project:
            return False
        
        self.db.delete(db_project)
        self.db.commit()
        return True

    def soft_delete(self, project_id: int) -> Optional[Project]:
        """Soft delete a project by setting is_active to False"""
        db_project = self.get_by_id(project_id)
        if not db_project:
            return None
        
        db_project.is_active = False
        self.db.commit()
        self.db.refresh(db_project)
        return db_project