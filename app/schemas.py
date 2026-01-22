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

class TicketSchema(BaseModel):
    id: int
    code: str
    voyageur: str
    validé: bool

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
