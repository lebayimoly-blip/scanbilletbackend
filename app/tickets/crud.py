from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import Ticket

def get_all_tickets(db: Session):
    return db.query(Ticket).all()

def create_ticket(db: Session, code: str, voyageur: str, user_id: int):
    existing = db.query(Ticket).filter(Ticket.code == code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ce code de ticket existe déjà")
    ticket = Ticket(code=code, voyageur=voyageur, user_id=user_id)
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket
