# Online Store REST API (FastAPI)

A RESTful API for an online store built with FastAPI.

This project is a new implementation of my Online Store REST API using FastAPI.
It demonstrates user authentication, database management, and REST API development with modern Python technologies.

 **Project Status:** In Progress

## Technologies

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pydantic
- JWT Authentication
- Swagger/OpenAPI
- Git

## Current Features

- JWT-based authentication and authorization
- User account management (profile update, password change, account deletion)
- Product management with CRUD operations
- Product categorization and search by name
- Order management (create, view, update status, and cancel orders)
- Automatic total price calculation and inventory updates when orders are created or cancelled
- Role-based access control (admins, employees, and customers have different permissions)
- Request and response validation using Pydantic
- Interactive API documentation with Swagger/OpenAPI

## Requirements

- Python 3.12+
- PostgreSQL
  
## Installation and Running

### 1. Clone the repository

```bash
git clone https://github.com/Sofia-so/fast_api_pet_project.git
cd fast_api_pet_project
```

### 2. Create and activate a virtual environment

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux/macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+psycopg://username:password@localhost:5432/database_name
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Run database migrations

```bash
alembic upgrade head
```

### 6. Start the application

```bash
uvicorn app.main:app --reload
```

The API will be available at:

- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Author

**Sofia Sudarkova**

GitHub: https://github.com/Sofia-so

Email: sudarkovasofia0@gmail.com  
