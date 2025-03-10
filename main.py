from fastapi import FastAPI, Depends, HTTPException
from user.models import User
from db_setup import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel
from sqlalchemy import insert

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World 434"}


@app.get("/cars")
def read_root():
    return {"Hello": "my cars"}

class UserCreate(BaseModel):
    name: str
    email: str
    password: str


@app.post("/users")
async def create_user(user_create: UserCreate, db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(User).filter_by(email=user_create.email))
    existing_user = result.scalars().first()

    if existing_user:
        print("User with this email already exists!")
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create a new user
    user = User(
        name=user_create.name, email=user_create.email, password=user_create.password
    )

    db.add(user)

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()  # In case of an error, rollback the transaction
        raise HTTPException(status_code=500, detail="Error saving user to the database")

    return {"message": "User created successfully", "user": user_create}
