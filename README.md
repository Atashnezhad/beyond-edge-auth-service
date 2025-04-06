# Beyond Edge Auth Service

A modern, edge-computing ready authentication service built with FastAPI and Python. test.

## Features

- 🔐 JWT-based authentication
- 👤 User registration and management
- 🔑 Secure password handling with bcrypt
- 📧 Email verification system
- 🔄 Password reset functionality
- 🛡️ Rate limiting and security features
- 📝 OpenAPI documentation
- 🧪 Comprehensive test suite

## Prerequisites

- Python 3.8+
- PostgreSQL
- Redis (for rate limiting)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Atashnezhad/beyond-edge-auth-service.git
cd beyond-edge-auth-service
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/MacOS
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Copy the example env file
cp .env.example .env

# Edit .env with your configuration
```

## Configuration

Create a `.env` file with the following variables:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-specific-password
```

## Running the Application

1. Start the server:
```bash
uvicorn app.main:app --reload
```

2. Stop the server:
```bash
# Windows
.\kill_server.bat

# Linux/MacOS
pkill -f uvicorn
```

The API will be available at `http://localhost:8000`

## API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Development

### Running Tests
```bash
pytest
```

### Code Style
This project uses:
- Black for code formatting
- Flake8 for linting
- MyPy for type checking

Run formatting:
```bash
black .
```

Run linting:
```bash
flake8
```

Run type checking:
```bash
mypy .
```

## Project Structure

```
beyond-edge-auth-service/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py
│   │       └── users.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── db/
│   │   ├── base.py
│   │   └── session.py
│   ├── models/
│   │   └── user.py
│   ├── schemas/
│   │   └── user.py
│   └── main.py
├── tests/
├── alembic/
├── .env.example
├── .gitignore
├── kill_server.bat
├── requirements.txt
└── README.md
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 