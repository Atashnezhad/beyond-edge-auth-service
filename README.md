# Beyond Edge Auth Service

This is the authentication service for the Beyond Edge application. It provides user registration, login, and token-based authentication using FastAPI and PostgreSQL.

## Features

- User registration with email and password
- JWT-based authentication
- PostgreSQL database integration
- Async database operations
- CORS support for frontend integration

## Prerequisites

- Python 3.8+
- PostgreSQL database
- Virtual environment (recommended)

## Setup

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory with the following variables:
```
DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

4. Initialize the database:
```bash
alembic upgrade head
```

## Running the Service

Start the service with:
```bash
uvicorn app.main:app --reload
```

The service will be available at `http://localhost:8000`

## API Documentation

Once the service is running, you can access:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

- `POST /auth/register` - Register a new user
- `POST /auth/token` - Login and get access token
- `GET /auth/users/me` - Get current user information

## Development

The project structure follows a modular design:
- `app/models/` - Pydantic models for request/response
- `app/services/` - Business logic
- `app/database/` - Database configuration and models
- `app/routers/` - API endpoints
- `app/main.py` - Application entry point

## Security Considerations

- Passwords are hashed using bcrypt
- JWT tokens are used for authentication
- CORS is configured for frontend integration
- Environment variables for sensitive data 