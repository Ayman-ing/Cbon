from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from app.core.database import get_db
from app.task.model import Task
from app.task.schema import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["Tasks"])


# Database operations
def create_task_in_db(db: Session, task_data: TaskCreate) -> Task:
    """Create a new task in the database"""
    db_task = Task(**task_data.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_task_by_id(db: Session, task_id: UUID) -> Optional[Task]:
    """Get a task by ID from the database"""
    return db.query(Task).filter(Task.id == task_id).first()


def get_all_tasks_from_db(db: Session, skip: int = 0, limit: int = 100, status_filter: Optional[str] = None) -> List[Task]:
    """Get all tasks from the database with optional filtering"""
    query = db.query(Task)
    if status_filter:
        query = query.filter(Task.status == status_filter)
    return query.offset(skip).limit(limit).all()


def update_task_in_db(db: Session, task_id: UUID, task_data: TaskUpdate) -> Optional[Task]:
    """Update a task in the database"""
    db_task = get_task_by_id(db, task_id)
    if not db_task:
        return None
    
    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task_by_id(db: Session, task_id: UUID) -> bool:
    """Delete a task from the database (hard delete)"""
    db_task = get_task_by_id(db, task_id)
    if not db_task:
        return False
    
    db.delete(db_task)
    db.commit()
    return True


def soft_delete_task_in_db(db: Session, task_id: UUID) -> Optional[Task]:
    """Soft delete a task by setting status to 'archived'"""
    db_task = get_task_by_id(db, task_id)
    if not db_task:
        return None
    
    db_task.status = 'archived'
    db.commit()
    db.refresh(db_task)
    return db_task


# API Routes
@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task"
)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new task with the following information:
    - **title**: Task title (required)
    - **description**: Task description (optional)
    - **status**: Task status (default: active)
    - **owner_id**: Task owner UUID (optional)
    """
    task = create_task_in_db(db, task_data)
    return TaskResponse.model_validate(task)


@router.get(
    "/",
    response_model=List[TaskResponse],
    summary="Get all tasks"
)
def get_all_tasks(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return"),
    status_filter: Optional[str] = Query(None, description="Filter tasks by status"),
    db: Session = Depends(get_db)
):
    """
    Retrieve all tasks with pagination and optional filtering.
    """
    tasks = get_all_tasks_from_db(db, skip=skip, limit=limit, status_filter=status_filter)
    return [TaskResponse.model_validate(t) for t in tasks]


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Get a task by ID"
)
def get_task(
    task_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific task by its ID.
    """
    task = get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return TaskResponse.model_validate(task)


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Update a task"
)
def update_task(
    task_id: UUID,
    task_data: TaskUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a task's information. Only provided fields will be updated.
    """
    task = update_task_in_db(db, task_id, task_data)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return TaskResponse.model_validate(task)


@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Partially update a task"
)
def patch_task(
    task_id: UUID,
    task_data: TaskUpdate,
    db: Session = Depends(get_db)
):
    """
    Partially update a task. Same as PUT but semantically indicates partial update.
    """
    task = update_task_in_db(db, task_id, task_data)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return TaskResponse.model_validate(task)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a task"
)
def delete_task(
    task_id: UUID,
    soft: bool = Query(False, description="Use soft delete (archive) instead of hard delete"),
    db: Session = Depends(get_db)
):
    """
    Delete a task. Use soft=true for soft delete (sets status to 'archived').
    """
    if soft:
        task = soft_delete_task_in_db(db, task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id {task_id} not found"
            )
        return {"message": "Task archived successfully"}
    else:
        deleted = delete_task_from_db(db, task_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id {task_id} not found"
            )
        return {"message": "Task deleted successfully"}
