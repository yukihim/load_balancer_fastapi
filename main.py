from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
import models
from database import engine, get_db, AsyncSessionLocal
import asyncio

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
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
        
    max_retries = 30
    for i in range(max_retries):
        try:
            async with AsyncSessionLocal() as db:
                result = await db.execute(select(models.User))
                users = result.scalars().all()
                if not users:
                    # Seed initial users
                    new_users = [
                        models.User(name="Alice"),
                        models.User(name="Bob")
                    ]
                    db.add_all(new_users)
                    await db.commit()
                    print("Seeded initial users: Alice and Bob")
            break
        except Exception as e:
            if i < max_retries - 1:
                print(f"Database not ready, retrying... ({i+1}/{max_retries}) | Error: {e}")
                await asyncio.sleep(1)
            else:
                print(f"Failed to connect to database after {max_retries} attempts")
                raise

@app.get("/")
async def read_root():
    """Root endpoint"""
    return {"message": "Welcome to User API"}

@app.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """Create a new user"""
    db_user = models.User(name=user.name)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

@app.get("/users/", response_model=list[UserResponse])
async def get_users(db: AsyncSession = Depends(get_db)):
    """Get all users"""
    result = await db.execute(select(models.User))
    return result.scalars().all()

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """Get a user by ID"""
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users/name/{name}", response_model=UserResponse)
async def get_user_by_name(name: str, db: AsyncSession = Depends(get_db)):
    """Get a user by name (retrieve name from database)"""
    result = await db.execute(select(models.User).filter(models.User.name == name))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with name '{name}' not found")
    return user
