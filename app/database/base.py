from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class DatabaseInterface(ABC):
    @abstractmethod
    async def connect(self) -> None:
        """Establish database connection"""
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """Close database connection"""
        pass

    @abstractmethod
    async def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user"""
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        pass

    @abstractmethod
    async def update_user(self, user_id: int, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update user data"""
        pass

    @abstractmethod
    async def delete_user(self, user_id: int) -> bool:
        """Delete user"""
        pass

    @abstractmethod
    async def list_users(self) -> List[Dict[str, Any]]:
        """List all users"""
        pass 