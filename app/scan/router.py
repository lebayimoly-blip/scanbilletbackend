from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Ticket

router = APIRouter()

@router.post("/scan/{code}")
def scan_ticket(code: str, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.code == code).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket non trouvé")
    if ticket.valide:
        raise HTTPException(status_code=400, detail="Ticket déjà validé")

    ticket.valide = True
    db.commit()
    return {"message": f"Ticket {code} validé avec succès"}

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Ticket

router = APIRouter()

@router.post("/scan/{code}")
def scan_ticket_path(code: str, db: Session = Depends(get_db)):
    return _validate_ticket(code, db)

@router.post("/scan")
def scan_ticket_json(payload: dict = Body(...), db: Session = Depends(get_db)):
    code = payload.get("code")
    if not code:
        raise HTTPException(status_code=422, detail="Champ 'code' requis")
    return _validate_ticket(code, db)

def _validate_ticket(code: str, db: Session):
    ticket = db.query(Ticket).filter(Ticket.code == code).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket non trouvé")
    if ticket.valide:
        raise HTTPException(status_code=400, detail="Ticket déjà validé")

    ticket.valide = True
    db.commit()
    return {"message": f"Ticket {code} validé avec succès"}
