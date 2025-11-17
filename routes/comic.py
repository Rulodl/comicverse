from fastapi import APIRouter, status, HTTPException
from models.comic import Comic,ComicUpdate
from controllers.comic import (get_all_comics
                                , create_comic
                                , update_comic
                                , delete_comic
                                , get_comic
                                , get_comic_pedidos
                                )


router = APIRouter(prefix="/comics")

@router.get("", tags=["Comics"], status_code=status.HTTP_200_OK)
async def get_all():
    """
    Devuelve todos los cómics registrados en la base de datos.
    """
    try:
        result = await get_all_comics()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener cómics: {str(e)}")

@router.post("", tags=["Comics"], status_code=status.HTTP_201_CREATED)
async def post_comic(comic: Comic):
    """
    Crea un nuevo cómic en la base de datos.
    """
    try:
        result = await create_comic(comic)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear cómic: {str(e)}")

@router.put("/{id_comic}", tags=["Comics"], status_code=status.HTTP_200_OK)
async def update_comic_information(id_comic: int, comic_data: ComicUpdate):
    """
    Actualiza un comic existente en la base de datos.
    """
    try:
        result = await update_comic(id_comic, comic_data)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar comic: {str(e)}")

@router.delete("/{id_comic}", tags=["Comics"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_comic_by_id(id_comic: int):
    """
    Elimina un cómic
    """
    await delete_comic(id_comic)

@router.get("/{id_comic}", tags=["Comics"], status_code=status.HTTP_200_OK)
async def get_comic_by_id(id_comic: int):
    """
    Obtiene un cómic por su id:
    """
    return await get_comic(id_comic)

@router.get("/{id_comic}/pedidos", tags=["Comics"], status_code=status.HTTP_200_OK)
async def get_comic_pedidos_by_id(id_comic: int):
    """
    Obtiene todos los pedidos en los que aparece un cómic específico.
    """
    return await get_comic_pedidos(id_comic)



