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

from app.models import Scan, User  # Assure-toi que c’est bien importé
from datetime import datetime

def _validate_ticket(code: str, db: Session):
    ticket = db.query(Ticket).filter(Ticket.code == code).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket non trouvé")
    if ticket.validé:
        raise HTTPException(status_code=400, detail="Ticket déjà validé")

    # Marquer le ticket comme validé
    ticket.validé = True

    # Récupérer l'utilisateur (si lié à une session ou token)
    # Ici on suppose un utilisateur par défaut pour l'exemple
    user = db.query(User).filter(User.username == "moly").first()  # à adapter selon ton auth

    # Créer un enregistrement de scan
    scan = Scan(
        ticket_id=ticket.id,
        user_id=user.id if user else None,
        timestamp=datetime.now(),
        validated=True
    )
    db.add(scan)
    db.commit()

    return {"message": f"Ticket {code} validé avec succès"}

