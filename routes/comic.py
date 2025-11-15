from fastapi import APIRouter, status, HTTPException
from controllers.comic import get_all_comics

router = APIRouter(prefix="/comics")

@router.get("/", tags=["Comics"], status_code=status.HTTP_200_OK)
async def get_all():
    """
    Devuelve todos los cómics registrados en la base de datos.
    """
    try:
        result = await get_all_comics()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener cómics: {str(e)}")
