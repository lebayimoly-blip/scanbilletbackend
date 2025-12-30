from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.auth.router import router as auth_router
from app.tickets.router import router as tickets_router
from app.scan.router import router as scan_router
from app.database import init_db

app = FastAPI()
init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tu peux restreindre à ["http://localhost:3000"] ou autre
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(tickets_router, prefix="/tickets", tags=["tickets"])
app.include_router(scan_router, prefix="/scan", tags=["scan"])

@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API ScanBillet"}
