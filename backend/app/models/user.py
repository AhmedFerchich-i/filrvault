from sqlalchemy import Column, Integer, String, DateTime
from core.db import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    username = Column(String,  index=True, nullable=True)  # optional display username
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
