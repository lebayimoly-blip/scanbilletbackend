from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.auth.utils import get_current_user
from app.scan.logic import validate_ticket  # logique métier centralisée

router = APIRouter()

@router.post("/{code}")
def scan_ticket_path(
    code: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    print(f"[SCAN PATH] Code reçu : {code}")
    return validate_ticket(code, db, current_user)

@router.post("/")
def scan_ticket_json(
    payload: dict = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    code = payload.get("code")
    if not code:
        raise HTTPException(status_code=422, detail="Champ 'code' requis")
    print(f"[SCAN JSON] Code reçu : {code}")
    return validate_ticket(code, db, current_user)
