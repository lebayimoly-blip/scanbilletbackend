from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import csv
from io import StringIO

from app.database import get_db
from app.models import Ticket
from app.tickets import crud
from app.schemas import TicketSchema, TicketCreate

router = APIRouter()

@router.get("/", response_model=List[TicketSchema])
def list_tickets(db: Session = Depends(get_db)):
    return crud.get_all_tickets(db)

@router.post("/", response_model=TicketSchema)
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    return crud.create_ticket(
        db,
        code=ticket.code,
        voyageur=ticket.voyageur,
        user_id=ticket.user_id
    )

@router.post("/import")
async def import_tickets(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Le fichier doit être un CSV")

    content = await file.read()
    decoded = content.decode("utf-8")
    reader = csv.DictReader(StringIO(decoded))

    imported = 0
    for row in reader:
        code = row.get("code")
        voyageur = row.get("voyageur")
        if code and voyageur:
            existing = db.query(Ticket).filter(Ticket.code == code).first()
            if not existing:
                ticket = Ticket(code=code, voyageur=voyageur)
                db.add(ticket)
                imported += 1

    db.commit()
    return {"message": f"{imported} billets importés avec succès"}

@router.get("/export", response_model=List[TicketSchema])
def export_valid_tickets(db: Session = Depends(get_db)):
    return db.query(Ticket).filter(Ticket.validé == True).all()
