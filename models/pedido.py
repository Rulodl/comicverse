
from typing import List, Optional
from datetime import date
from pydantic import BaseModel, Field

# Creación de pedido

class ComicPedido(BaseModel):
    id_comic: int = Field(..., examples=[1])
    cantidad_comics: int = Field(..., gt=0, examples=[2])

class PedidoCreate(BaseModel):
    id_cliente: int = Field(..., examples=[1])
    fecha_entrega: Optional[str] = Field(
        default=None,
        pattern=r"^\d{4}-\d{2}-\d{2}$",
        examples=["2025-11-20"]
    )
    comics: List[ComicPedido]

# Actualización de pedido

class ComicPedidoUpdate(BaseModel):
    id_comic: int
    cantidad_comics: Optional[int] = None
    estado: Optional[str] = None

class PedidoUpdate(BaseModel):
    fecha_entrega: Optional[date] = None
    comics: Optional[List[ComicPedidoUpdate]] = None

# Reemplazo de cómic

class ComicReplace(BaseModel):
    id_comic_nuevo: int
    cantidad_comics: int = Field(..., gt=0)
    estado: Optional[str] = None

# Actualización de estado

class ComicEstadoUpdate(BaseModel):
    id_comic: int
    estado: Optional[str] = None

class PedidoEstadoUpdate(BaseModel):
    fecha_entrega: Optional[date] = None
    comics: Optional[List[ComicEstadoUpdate]] = None
