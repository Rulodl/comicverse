from pydantic import BaseModel, EmailStr
from typing import Optional

class Cliente(BaseModel):

    nombre: str
    apellido: Optional[str] = None
    email: Optional[EmailStr] = None

class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    email: Optional[EmailStr] = None