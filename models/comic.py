from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class Comic(BaseModel):
    num_comic: Optional[int] = None
    titulo: str  # obligatorio
    id_editorial: int  # obligatorio
    id_autor: int  # obligatorio
    fecha_publicacion: Optional[str] = None
    inventario: int  # obligatorio




class ComicUpdate(BaseModel):
    num_comic: Optional[int] = None
    titulo: Optional[str] = None
    id_editorial: Optional[int] = None
    id_autor: Optional[int] = None
    fecha_publicacion: Optional[date] = None
    inventario: Optional[int] = Field(0, ge=0)  # cantidad a sumar

