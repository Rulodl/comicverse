from fastapi import APIRouter, status, HTTPException
from typing import List
from controllers.cliente import get_all_clientes
from models.cliente import Cliente

router = APIRouter(prefix="/clientes")

@router.get("/", tags=["Clientes"], status_code=status.HTTP_200_OK)
async def get_all():
    """
    Devuelve todos los clientes registrados en la base de datos.
    """
    result = await get_all_clientes()
    return result


