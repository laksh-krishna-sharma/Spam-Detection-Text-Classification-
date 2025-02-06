from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session
import bcrypt
from models import User, Messages  # Ensure models are defined correctly
from database import SessionLocal, engine  # Adjust imports as needed
from fastapi.middleware.cors import CORSMiddleware
from celery import Celery
from celery_worker import predict_spam

celery_app = Celery(
    "worker", 
    backend="redis://localhost:6379/0", 
    broker="redis://localhost:6379/0"
)
# Initialize FastAPI app
app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app URL during development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables if they don't exist
User.metadata.create_all(bind=engine)
Messages.metadata.create_all(bind=engine)

# Pydantic Models for input data
class Message(BaseModel):
    text: str
    user_id: int  # Include user_id in the Message model

class UserCreate(BaseModel):
    username: str
    password: str

class UserSignin(BaseModel):
    username: str
    password: str

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# Utility for hashing passwords
def hash_password(password: str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# Root Endpoint
@app.get("/")
def index():
    return {"message": "Spam Detection and User Management API"}

# User Signup Endpoint
@app.post("/signup/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = db.query(User).filter(User.username == user.username).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Username already taken")
        
        hashed_password = hash_password(user.password)
        db_user = User(username=user.username, password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {"id": db_user.id, "username": db_user.username}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# User Signin Endpoint
@app.post("/signin/")
def signin(user: UserSignin, db: Session = Depends(get_db)):
    try:
        db_user = db.query(User).filter(User.username == user.username).first()
        if not db_user or not verify_password(user.password, db_user.password):
            raise HTTPException(status_code=400, detail="Invalid username or password")
        
        return {"message": "Signin successful", "user_id": db_user.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Spam Prediction and Message Saving Endpoint
@app.post("/predict")
async def predict_message(message: Message, db: db_dependency):
    user = db.query(User).filter(User.id == message.user_id).first()
    
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    # Enqueue task
    task = predict_spam.delay(message.text, message.user_id)

    return {"task_id": task.id, "message": "Prediction task started"}

# Route to get all Messages for a user
@app.get("/users/{user_id}/messages")
def get_user_messages(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user.messages  # Ensure that User model has a relationship with Messages

# Start the server when running the script
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
