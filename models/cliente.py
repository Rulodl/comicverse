from pydantic import BaseModel, Field
from typing import Optional

class Cliente(BaseModel):

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
        pattern=r"^[\\w\\.-]+@[\\w\\.-]+\\.\\w{2,}$",
        examples=["cliente@comicverse.com", "maria.perez@gmail.com"]
    )
