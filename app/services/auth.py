from datetime import datetime, timedelta
from typing import Optional, List
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status

from ..models.user import User, TokenData
from ..database.base import DatabaseInterface

# Security configuration
SECRET_KEY = "your-secret-key-here"  # In production, use environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Define available scopes
SCOPES = {
    "read": "Read access",
    "write": "Write access",
    "admin": "Administrative access"
}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, db: DatabaseInterface):
        self.db = db

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def create_access_token(self, data: dict, scopes: List[str] = None, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({
            "exp": expire,
            "scopes": scopes or ["read"]  # Default to read scope if none specified
        })
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user = await self.db.get_user_by_email(email)
        if not user:
            return None
        if not self.verify_password(password, user["hashed_password"]):
            return None
        return User(**user)

    async def create_user(self, email: str, password: str, full_name: str) -> User:
        # Check if user already exists
        existing_user = await self.db.get_user_by_email(email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Create new user
        hashed_password = self.get_password_hash(password)
        user_data = {
            "email": email,
            "hashed_password": hashed_password,
            "full_name": full_name
        }
        user = await self.db.create_user(user_data)
        return User(**user)

    async def get_current_user(self, token: str, required_scopes: List[str] = None) -> User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
            
            # Check scopes if required
            if required_scopes:
                token_scopes = payload.get("scopes", [])
                if not all(scope in token_scopes for scope in required_scopes):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Not enough permissions",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
            
            token_data = TokenData(email=email)
        except JWTError:
            raise credentials_exception

        user = await self.db.get_user_by_email(email=token_data.email)
        if user is None:
            raise credentials_exception
        return User(**user) 