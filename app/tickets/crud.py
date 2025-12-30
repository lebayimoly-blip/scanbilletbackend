from sqlalchemy.orm import Session
from app.models import Ticket

def get_all_tickets(db: Session):
    return db.query(Ticket).all()

def create_ticket(db: Session, code: str, voyageur: str):
    existing = db.query(Ticket).filter(Ticket.code == code).first()
    if existing:
        raise ValueError("Ce code de ticket existe déjà")
    ticket = Ticket(code=code, voyageur=voyageur)
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket
