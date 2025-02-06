from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# User Model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(128), nullable=False)

    # Relationship with Messages table
    messages = relationship("Messages", back_populates="user", cascade="all, delete-orphan")


# Messages Model
class Messages(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    labels = Column(String(50), nullable=False)
    text = Column(String(1000), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Relationship with User table
    user = relationship("User", back_populates="messages")
