from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re


class Autor(BaseModel):
    id_autor: Optional[int] = Field(
        default=None,
        description="ID autoincrementable del autor"
    )

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

    nacionalidad: Optional[str] = Field(
        default=None,
        description="Nacionalidad del autor",
        pattern=r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]+$",
        examples=["Estadounidense", "Británico"]
    )
