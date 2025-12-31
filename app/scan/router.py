from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Ticket

router = APIRouter()

@router.post("/{code}")
def scan_ticket_path(code: str, db: Session = Depends(get_db)):
    print(f"[SCAN PATH] Code reçu : {code}")
    return _validate_ticket(code, db)

@router.post("/")
def scan_ticket_json(payload: dict = Body(...), db: Session = Depends(get_db)):
    code = payload.get("code")
    if not code:
        raise HTTPException(status_code=422, detail="Champ 'code' requis")
    print(f"[SCAN JSON] Code reçu : {code}")
    return _validate_ticket(code, db)

def _validate_ticket(code: str, db: Session):
    ticket = db.query(Ticket).filter(Ticket.code == code).first()
    if not ticket:
        print(f"[SCAN] Ticket {code} introuvable")
        raise HTTPException(status_code=404, detail="Ticket non trouvé")
    if ticket.validé:
        print(f"[SCAN] Ticket {code} déjà validé")
        raise HTTPException(status_code=400, detail="Ticket déjà validé")

    ticket.validé = True
    db.commit()
    print(f"[SCAN] Ticket {code} validé avec succès")
    return {"message": f"Ticket {code} validé avec succès"}
