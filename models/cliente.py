from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re


class Cliente(BaseModel):
    id_cliente: Optional[int] = Field(
        default=None,
        description="ID autoincrementable del cliente"
    )

    nombre: Optional[str] = Field(
        default=None,
        description="Nombre del cliente",
        pattern=r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]+$",
        examples=["Carlos", "María", "Luis"]
    )

    apellido: Optional[str] = Field(
        default=None,
        description="Apellido del cliente",
        pattern=r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]+$",
        examples=["Hernández", "Pérez"]
    )

    email: Optional[str] = Field(
        default=None,
        description="Correo electrónico del cliente",
        pattern=r"^[\w\.-]+@[\w\.-]+\.\w{2,}$",
        examples=["cliente@example.com"]
    )