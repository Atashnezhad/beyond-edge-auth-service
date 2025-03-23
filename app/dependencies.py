import os
from dotenv import load_dotenv
from .database.postgres import PostgresDatabase
from .services.auth import AuthService

# Load environment variables
load_dotenv()

# Initialize database
database = PostgresDatabase(os.getenv("DATABASE_URL"))
auth_service = AuthService(database) 