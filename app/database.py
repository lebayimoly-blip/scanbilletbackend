from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Charger les variables d'environnement en local (.env)
load_dotenv()

# Récupérer l'URL de la base (Render ou local)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://scanticket_user:okGEVWVJpyjphtXu4ETTi0FUoBDTGSv8@dpg-d91r8f9kh4rs73ar3mtg-a.oregon-postgres.render.com/scanticket?sslmode=require"
)

# ✅ Création du moteur avec SSL obligatoire
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800,
    connect_args={"sslmode": "require"}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Création automatique des tables au démarrage
def init_db():
    from app import models  # Assure que les modèles sont importés
    Base.metadata.create_all(bind=engine)
