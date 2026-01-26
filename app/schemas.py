from pydantic import BaseModel
from datetime import datetime

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreate(BaseModel):
    username: str
    password: str

class TicketCreate(BaseModel):
    code: str
    voyageur: str
    user_id: int

class TicketSchema(BaseModel):
    id: int
    code: str
    voyageur: str
    validé: bool
    scanne: bool
    created_at: datetime

    class Config:
        orm_mode = True

class ScanSchema(BaseModel):
    id: int
    ticket_id: int
    user_id: int
    timestamp: datetime
    validated: bool

    class Config:
        orm_mode = True
