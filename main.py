from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models
from database import engine, get_db
import time

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="User API", description="Simple API to manage users in PostgreSQL")

# Pydantic schemas
class UserCreate(BaseModel):
    name: str

class UserResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

@app.on_event("startup")
async def startup_event():
    """Wait for database to be ready and seed initial data"""
    max_retries = 30
    for i in range(max_retries):
        try:
            db = next(get_db())
            # Check if we have any users, if not seed some data
            user_count = db.query(models.User).count()
            if user_count == 0:
                # Seed initial users
                users = [
                    models.User(name="Alice"),
                    models.User(name="Bob")
                ]
                db.add_all(users)
                db.commit()
                print("Seeded initial users: Alice and Bob")
            db.close()
            break
        except Exception as e:
            if i < max_retries - 1:
                print(f"Database not ready, retrying... ({i+1}/{max_retries})")
                time.sleep(1)
            else:
                print(f"Failed to connect to database after {max_retries} attempts")
                raise

@app.get("/")
def read_root():
    """Root endpoint"""
    return {"message": "Welcome to User API"}

@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    db_user = models.User(name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    """Get all users"""
    users = db.query(models.User).all()
    return users

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get a user by ID"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users/name/{name}", response_model=UserResponse)
def get_user_by_name(name: str, db: Session = Depends(get_db)):
    """Get a user by name (retrieve name from database)"""
    user = db.query(models.User).filter(models.User.name == name).first()
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with name '{name}' not found")
    return user
