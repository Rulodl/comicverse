from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re


class Comic(BaseModel):

    num_comic: Optional[int] = Field(
        default=None,
        description="Número del cómic",
        examples=[1, 25, 300]
    )

    titulo: Optional[str] = Field(
        default=None,
        description="Título del cómic",
        min_length=1,
        max_length=200,
        examples=["Spider-Man", "Batman", "The Walking Dead"]
    )

    editorial_id: Optional[int] = Field(
        default=None,
        description="FK hacia la tabla editorial (id_editorial)",
        examples=[1]
    )

    autor_id: Optional[int] = Field(
        default=None,
        description="FK hacia la tabla autor (id_autor)",
        examples=[1]
    )

    fecha_publicacion: Optional[str] = Field(
        default=None,
        description="Fecha de publicación en formato YYYY-MM-DD",
        pattern=r"^\d{4}-\d{2}-\d{2}$",
        examples=["2022-05-10"]
    )

    inventario: Optional[int] = Field(
        default=0
        ,description="Cantidad de ejemplares en inventario",
        examples=[0, 5, 10] 
    )
