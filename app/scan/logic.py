# Ce fichier peut contenir des fonctions de traitement avancé
# Exemple : vérification de validité, logs, etc.

from datetime import datetime
from fastapi import HTTPException
from app.models import Scan, Ticket, User

def is_ticket_valid(ticket):
    return not ticket.validé

def validate_ticket(code: str, db, current_user: User):
    # 1. Rechercher le billet
    ticket = db.query(Ticket).filter(Ticket.code == code).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket non trouvé")

    # 2. Vérifier s’il est déjà validé
    if ticket.validé:
        raise HTTPException(status_code=400, detail="Ticket déjà validé")

    # 3. Marquer comme validé
    ticket.validé = True

    # 4. Créer un enregistrement de scan avec l’utilisateur connecté
    scan = Scan(
        ticket_id=ticket.id,
        user_id=current_user.id,
        timestamp=datetime.now(),
        validated=True
    )
    db.add(scan)
    db.commit()

    return {"message": f"Ticket {code} validé avec succès"}
