from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re


class Pedido(BaseModel):
    id_pedido: Optional[int] = Field(
        default=None,
        description="ID autoincrementable del pedido"
    )

    cliente_id: Optional[int] = Field(
        default=None,
        description="FK hacia la tabla cliente (id_cliente)",
        examples=[1]
    )

    fecha_pedido: Optional[str] = Field(
        default=None,
        description="Fecha del pedido en formato YYYY-MM-DD",
        pattern=r"^\d{4}-\d{2}-\d{2}$",
        examples=["2025-11-13"]
    )

    fecha_entrega: Optional[str] = Field(
        default=None,
        description="Fecha estimada de entrega en formato YYYY-MM-DD",
        pattern=r"^\d{4}-\d{2}-\d{2}$",
        examples=["2025-11-20"]
    )
