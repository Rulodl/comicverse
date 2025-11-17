from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class Comic(BaseModel):
    num_comic: Optional[int] = None
    titulo: str
    id_editorial: int  
    id_autor: int  
    fecha_publicacion: Optional[str] = None
    inventario: int  



class ComicUpdate(BaseModel):
    num_comic: Optional[int] = None
    titulo: Optional[str] = None
    id_editorial: Optional[int] = None
    id_autor: Optional[int] = None
    fecha_publicacion: Optional[date] = None
    inventario: Optional[int] = Field(0, ge=0)

