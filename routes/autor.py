from fastapi import APIRouter, status, HTTPException
from controllers.autor import get_all_autores

router = APIRouter(prefix="/autores")

@router.get("/", tags=["Autores"], status_code=status.HTTP_200_OK)
async def get_all():
    """
    Devuelve todos los autores registrados en la base de datos.
    """
    try:
        result = await get_all_autores()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener autores: {str(e)}")
