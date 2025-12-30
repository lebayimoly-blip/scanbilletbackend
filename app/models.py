from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    voyageur = Column(String)
    validé = Column(Boolean, default=False)
