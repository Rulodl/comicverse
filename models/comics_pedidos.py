from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re


class ComicsPedidos(BaseModel):
    id_pedido: Optional[int] = Field(
        default=None,
        description="FK hacia la tabla pedido (id_pedido)",
        examples=[1]
    )

    id_comic: Optional[int] = Field(
        default=None,
        description="FK hacia la tabla comic (id_comic)",
        examples=[1]
    )

    cantidad_comics: Optional[int] = Field(
        default=None,
        description="Cantidad de copias del cómic dentro del pedido",
        examples=[1, 3, 10]
    )

    estado: Optional[str] = Field(
        default=None,
        description="Estado del cómic dentro del pedido",
        examples=["pendiente", "confirmado", "enviado"]
    )
