from pydantic import BaseModel, EmailStr


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str


class UserRegister(BaseModel):
    """Schema for user registration"""
    email: EmailStr
    password: str
    full_name: str


class Token(BaseModel):
    """Schema for authentication token response"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for token payload data"""
    user_id: str
    email: str
