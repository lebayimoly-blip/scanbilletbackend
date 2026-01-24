from app.database import SessionLocal
from app.models import User
from app.auth.utils import get_password_hash

# Crée une session DB
db = SessionLocal()

# Nom d'utilisateur à créer
username = "onangasetrag"

# Vérifie si l'utilisateur existe déjà
existing_user = db.query(User).filter(User.username == username).first()
if existing_user:
    print(f"Utilisateur déjà existant : {existing_user.username}")
else:
    # Hash du mot de passe
    hashed_pw = get_password_hash("Setrag2025.")

    # Création de l'utilisateur
    user = User(username=username, hashed_password=hashed_pw)
    db.add(user)
    db.commit()
    db.refresh(user)
    print("Utilisateur créé avec succès :", user.username)

db.close()
