from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserLogin, Token
from app.auth.utils import verify_password, create_access_token

router = APIRouter()

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Identifiants invalides")
    
    token = create_access_token(data={"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}

from app.auth.utils import get_password_hash
from app.schemas import UserCreate
from app.models import User

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Nom d'utilisateur déjà pris")

    hashed_pw = get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Utilisateur créé avec succès"}
