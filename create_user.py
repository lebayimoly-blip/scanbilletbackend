from app.database import SessionLocal
from app.models import User
from app.auth.utils import get_password_hash

# Crée une session DB
db = SessionLocal()

# Vérifie si l'utilisateur existe déjà
existing_user = db.query(User).filter(User.username == "lebayi moly").first()
if existing_user:
    print("Utilisateur déjà existant.")
else:
    # Hash du mot de passe
    hashed_pw = get_password_hash("Google99.")

    # Création de l'utilisateur
    user = User(username="lebayi moly", hashed_password=hashed_pw)
    db.add(user)
    db.commit()
    db.refresh(user)
    print("Utilisateur créé avec succès :", user.username)

db.close()
