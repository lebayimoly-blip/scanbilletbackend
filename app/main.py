import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.router import router as auth_router
from app.tickets.router import router as tickets_router
from app.scan.router import router as scan_router
from app.database import init_db
from app.scan import stats # ← ici on importe le fichier stats.py

# Initialisation de l'application
app = FastAPI()

# Initialisation de la base de données
init_db()

origins = [
    "http://localhost:27170",  # Flutter Web local
    "https://scanbilletfrontend.onrender.com",  # ton frontend déployé (si applicable)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routes
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(tickets_router, prefix="/tickets", tags=["tickets"])
app.include_router(scan_router, prefix="/scan", tags=["scan"])
app.include_router(stats.router, prefix="/stats", tags=["stats"])

# Route racine
@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API ScanBillet"}

# Lancement local
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
