from sqlalchemy import Column, String, Boolean, Integer, DateTime, Enum as SqlEnum
from sqlalchemy.sql import func
from app.db.database import Base
from enum import Enum

class UserRole(str, Enum):
    superuser = "superuser"
    admin = "admin"
    staff = "staff"
    user = "user"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    role = Column(SqlEnum(UserRole), default=UserRole.user)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

