from pydantic import BaseModel

class ClientCreate(BaseModel):
    name: str
    email: str
    age: int

class ClientOut(BaseModel):
    id: int
    name: str
    email: str
    age: int

    class Config:
        orm_mode = True
