from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class AutorCreate(BaseModel):

    nombre: Optional[str] = Field(
        default=None,
        description="Nombre del autor",
        pattern=r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]+$",
        examples=["Stan", "Frank", "Alan"]
    )

    apellido: Optional[str] = Field(
        default=None,
        description="Apellido del autor",
        pattern=r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]+$",
        examples=["Lee", "Miller", "Moore"]
    )

    email: Optional[str] = Field(
        default=None,
        description="Correo electrónico del autor",
        pattern=r"^[\w\.-]+@[\w\.-]+\.\w{2,}$",
        examples=["stan.lee@example.com"]
    )

class AutorUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    email: Optional[EmailStr] = None
