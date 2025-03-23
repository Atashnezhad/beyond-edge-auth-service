from typing import Any, Dict, List, Optional
from sqlalchemy import create_engine, Column, Integer, String, DateTime, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base
from datetime import datetime

from .base import DatabaseInterface

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PostgresDatabase(DatabaseInterface):
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine = None
        self.SessionLocal = None

    async def connect(self) -> None:
        self.engine = create_async_engine(self.database_url)
        self.SessionLocal = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def disconnect(self) -> None:
        if self.engine:
            await self.engine.dispose()

    async def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        async with self.SessionLocal() as session:
            now = datetime.utcnow()
            user = User(
                email=user_data["email"],
                hashed_password=user_data["hashed_password"],
                full_name=user_data["full_name"],
                created_at=now,
                updated_at=now
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "created_at": user.created_at,
                "updated_at": user.updated_at
            }

    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        async with self.SessionLocal() as session:
            result = await session.execute(select(User).filter(User.email == email))
            user = result.scalar_one_or_none()
            if user:
                return {
                    "id": user.id,
                    "email": user.email,
                    "hashed_password": user.hashed_password,
                    "full_name": user.full_name,
                    "created_at": user.created_at,
                    "updated_at": user.updated_at
                }
            return None

    async def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        async with self.SessionLocal() as session:
            result = await session.execute(select(User).filter(User.id == user_id))
            user = result.scalar_one_or_none()
            if user:
                return {
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                    "created_at": user.created_at,
                    "updated_at": user.updated_at
                }
            return None

    async def update_user(self, user_id: int, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        async with self.SessionLocal() as session:
            result = await session.execute(select(User).filter(User.id == user_id))
            user = result.scalar_one_or_none()
            if user:
                for key, value in user_data.items():
                    setattr(user, key, value)
                user.updated_at = datetime.utcnow()  # Update the timestamp
                await session.commit()
                await session.refresh(user)
                return {
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                    "created_at": user.created_at,
                    "updated_at": user.updated_at
                }
            return None

    async def delete_user(self, user_id: int) -> bool:
        async with self.SessionLocal() as session:
            result = await session.execute(select(User).filter(User.id == user_id))
            user = result.scalar_one_or_none()
            if user:
                await session.delete(user)
                await session.commit()
                return True
            return False

    async def list_users(self) -> List[Dict[str, Any]]:
        async with self.SessionLocal() as session:
            result = await session.execute(select(User))
            users = result.scalars().all()
            return [
                {
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                    "created_at": user.created_at,
                    "updated_at": user.updated_at
                }
                for user in users
            ] 