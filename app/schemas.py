from pydantic import BaseModel

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreate(BaseModel):
    username: str
    password: str

from pydantic import BaseModel

class TicketSchema(BaseModel):
    id: int
    code: str
    voyageur: str
    validé: bool

    class Config:
        orm_mode = True
