from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# User Model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(128), nullable=False) 
    
class messages(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    labels = Column(String(50), nullable=False)
    text = Column(String(1000))  
    user_id = Column(Integer, ForeignKey("users.id"))  