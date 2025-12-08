from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.core.database import get_db
from app.core.security import get_password_hash, get_current_user
from app.user.model import User
from app.user.schema import UserCreate, UserUpdate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


# Database operations
def create_user_in_db(db: Session, user_data: UserCreate) -> User:
    """Create a new user in the database"""
    user_dict = user_data.model_dump()
    user_dict['password_hash'] = get_password_hash(user_dict.pop('password'))
    db_user = User(**user_dict)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_id(db: Session, user_id: UUID) -> User | None:
    """Get a user by ID from the database"""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    """Get a user by email from the database"""
    return db.query(User).filter(User.email == email).first()


def get_all_users_from_db(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """Get all users from the database"""
    return db.query(User).offset(skip).limit(limit).all()


def update_user_in_db(db: Session, user_id: UUID, user_data: UserUpdate) -> User | None:
    """Update a user in the database"""
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    
    update_data = user_data.model_dump(exclude_unset=True)
    if 'password' in update_data:
        update_data['password_hash'] = get_password_hash(update_data.pop('password'))
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user_from_db(db: Session, user_id: UUID) -> bool:
    """Delete a user from the database"""
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True


# API Routes
@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user"
)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new user with the following information:
    - **email**: User email (required, unique)
    - **full_name**: User full name (optional)
    - **password**: User password (required, min 6 characters)
    """
    # Check if user already exists
    existing_user = get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    user = create_user_in_db(db, user_data)
    return UserResponse.model_validate(user)


@router.get(
    "/",
    response_model=List[UserResponse],
    summary="Get all users"
)
def get_all_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Retrieve all users with pagination.
    """
    users = get_all_users_from_db(db, skip=skip, limit=limit)
    return [UserResponse.model_validate(u) for u in users]


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get a user by ID"
)
def get_user(
    user_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific user by their ID.
    """
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return UserResponse.model_validate(user)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Update a user"
)
def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a user's information. Only provided fields will be updated.
    """
    user = update_user_in_db(db, user_id, user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return UserResponse.model_validate(user)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a user"
)
def delete_user(
    user_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Delete a user from the system.
    """
    deleted = delete_user_from_db(db, user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return {"message": "User deleted successfully"}
