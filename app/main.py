import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.router import router as auth_router
from app.tickets.router import router as tickets_router
from app.scan.router import router as scan_router
from app.database import init_db

# Initialisation de l'application
app = FastAPI()

# Initialisation de la base de données
init_db()

# Configuration des origines autorisées (CORS)
origins = (
    ["*"]
    if os.getenv("ENV") != "production"
    else ["https://ton-app-render.com"]
)

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

# Route racine
@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API ScanBillet"}

# Lancement local
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
