from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from app.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    scans = relationship("Scan", back_populates="user")
    hashed_password = Column(String)

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    voyageur = Column(String)
    validé = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow) # ✅ Ajout ici

class Scan(Base):
    __tablename__ = "scans"

    id = Column(Integer, primary_key=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    validated = Column(Boolean, default=False)

    user = relationship("User", back_populates="scans")
