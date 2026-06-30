from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Ticket
from app.tickets import crud

router = APIRouter()

from typing import List
from app.schemas import TicketSchema  # Assure-toi d'importer le schéma

@router.get("/", response_model=List[TicketSchema])
def list_tickets(db: Session = Depends(get_db)):
    return crud.get_all_tickets(db)

@router.post("/")
def create_ticket(code: str, voyageur: str, db: Session = Depends(get_db)):
    return crud.create_ticket(db, code=code, voyageur=voyageur)

from fastapi import UploadFile, File
import csv
from io import StringIO

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
