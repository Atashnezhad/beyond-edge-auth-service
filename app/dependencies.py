import os
from dotenv import load_dotenv
from .database.postgres import PostgresDatabase
from .services.auth import AuthService

# Load environment variables
load_dotenv()

def get_database_url() -> str:
    """Get database URL from environment variables."""
    # Try Railway's environment variable first
    database_url = os.getenv("RAILWAY_DATABASE_URL")
    if not database_url:
        # Fall back to local development URL
        database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("No database URL found in environment variables")
    return database_url

# Initialize database
database = PostgresDatabase(get_database_url())
auth_service = AuthService(database) 