from pydantic import BaseModel, Field, field_validator, HttpUrl
from typing import Optional
from datetime import date


class Editorial(BaseModel):
    
    nombre: Optional[str] = Field(
        default=None,
        description="Nombre de la editorial",
        pattern=r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9'()., -]+$",
        examples=["Marvel", "DC Comics", "Editorial Norma"]
    )

    fecha_fundacion: Optional[str] = Field(
        default=None,
        description="Fecha de fundación en formato YYYY-MM-DD",
        pattern=r"^\d{4}-\d{2}-\d{2}$",
        examples=["1961-08-01"]
    )

    sitio_web: Optional[str] = Field(
        default=None,
        description="Sitio web oficial de la editorial",
        pattern=r"^https?:\/\/[\w\-\.]+\.\w{2,}(\/.*)?$",
        examples=["https://www.marvel.com", "https://www.dc.com"]
    )

class EditorialUpdate(BaseModel):
    nombre: Optional[str] = None
    fecha_fundacion: Optional[date] = None
    sitio_web: Optional[str] = Field(
        default=None,
        description="Sitio web oficial de la editorial",
        pattern=r"^https?:\/\/[\w\-\.]+\.\w{2,}(\/.*)?$",
        examples=["https://www.marvel.com", "https://www.dc.com"]
    )