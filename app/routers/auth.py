from datetime import timedelta
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Body, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from ..models.user import User, UserCreate, Token
from ..services.auth import ACCESS_TOKEN_EXPIRE_MINUTES, SCOPES
from ..dependencies import auth_service

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes=SCOPES
)

# Example values for Swagger UI
EXAMPLE_USER = {
    "email": "test@example.com",
    "password": "testpassword",
    "full_name": "Test User"
}

EXAMPLE_TOKEN = {
    "username": "test@example.com",
    "password": "testpassword",
    "scope": "read write admin"
}

@router.post("/register", response_model=User)
async def register(user: UserCreate = Body(..., example=EXAMPLE_USER)):
    """Register a new user"""
    return await auth_service.create_user(
        email=user.email,
        password=user.password,
        full_name=user.full_name
    )

@router.post("/token", response_model=Token)
async def login(
    username: str = Form(..., example="test@example.com"),
    password: str = Form(..., example="testpassword"),
    scope: str = Form("read write admin", example="read write admin")
):
    """Login and get access token"""
    user = await auth_service.authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get requested scopes or default to read
    requested_scopes = scope.split() if scope else ["read"]
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": user.email},
        scopes=requested_scopes,
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=User)
async def read_users_me(token: str = Depends(oauth2_scheme)):
    """Get current user information"""
    return await auth_service.get_current_user(token)

@router.get("/users", response_model=List[User])
async def list_users(token: str = Depends(oauth2_scheme)):
    """List all users (requires admin scope)"""
    await auth_service.get_current_user(token, required_scopes=["admin"])
    return await auth_service.db.list_users() 