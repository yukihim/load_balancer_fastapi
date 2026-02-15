# load_balancer_fastapi

A simple FastAPI backend with Docker Compose and PostgreSQL database to manage users.

## Features

- FastAPI backend with RESTful API
- PostgreSQL database with Docker Compose
- User model with id and name fields
- CRUD operations for users
- Automatic database initialization with seed data

## Prerequisites

- Docker
- Docker Compose

## Getting Started

1. Clone the repository:
```bash
git clone https://github.com/yukihim/load_balancer_fastapi.git
cd load_balancer_fastapi
```

2. Start the application using Docker Compose:
```bash
docker-compose up --build
```

3. The API will be available at `http://localhost:8000`

## API Endpoints

- `GET /` - Root endpoint with welcome message
- `GET /users/` - Get all users
- `GET /users/{user_id}` - Get a user by ID
- `GET /users/name/{name}` - Get a user by name (retrieve name from database)
- `POST /users/` - Create a new user

### Example Usage

Get all users:
```bash
curl http://localhost:8000/users/
```

Get user by name:
```bash
curl http://localhost:8000/users/name/Alice
```

Create a new user:
```bash
curl -X POST http://localhost:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Charlie"}'
```

## Interactive API Documentation

FastAPI provides automatic interactive API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Stopping the Application

```bash
docker-compose down
```

To remove volumes as well:
```bash
docker-compose down -v
```

## Database

- Database: PostgreSQL 15
- Default credentials:
  - User: postgres
  - Password: postgres
  - Database: userdb
- Port: 5432

The application automatically seeds two users (Alice and Bob) on first startup.