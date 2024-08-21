# models.py

from sqlalchemy import Column, DateTime, Integer, String, Boolean
from app.database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user")  # Adicione um campo para a role do usuário (ex: "user", "admin")
    last_activity = Column(DateTime, default=datetime.utcnow)  # Novo campo
