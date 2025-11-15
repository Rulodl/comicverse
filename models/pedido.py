from pydantic import BaseModel, Field
from typing import Optional, List

class ComicPedido(BaseModel):
    id_comic: int = Field(
        ...,
        description="FK hacia la tabla comic (id_comic)",
        examples=[1]
    )
    cantidad_comics: int = Field(
        ...,
        description="Cantidad de ejemplares solicitados",
        gt=0,
        examples=[2]
    )

class PedidoCreate(BaseModel):
    cliente_id: int = Field(
        ...,
        description="FK hacia la tabla cliente (id_cliente)",
        examples=[1]
    )
    fecha_entrega: Optional[str] = Field(
        default=None,
        description="Fecha estimada de entrega en formato YYYY-MM-DD",
        pattern=r"^\d{4}-\d{2}-\d{2}$",
        examples=["2025-11-20"]
    )
    comics: List[ComicPedido] = Field(
        ...,
        description="Lista de cómics asociados al pedido"
    )
