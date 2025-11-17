from fastapi import APIRouter, status, HTTPException
from models.autor import AutorUpdate, AutorCreate
from controllers.autor import (get_all_autores, update_autor, get_autor
                                , delete_autor
                                , create_autor
                                , get_autor_comics
                                )


router = APIRouter(prefix="/autores")

@router.get("", tags=["Autores"], status_code=status.HTTP_200_OK)
async def get_all():
    """
    Devuelve todos los autores registrados en la base de datos.
    """
    try:
        result = await get_all_autores()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener autores: {str(e)}")

@router.put("/{id_autor}", tags=["Autores"], status_code=status.HTTP_200_OK)
async def update_autor_information(id_autor: int, autor_data: AutorUpdate):
    """
    Actualiza un autor existente en la base de datos.
    """
    try:
        result = await update_autor(id_autor, autor_data)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar autor: {str(e)}")

@router.get("/{id_autor}",tags=["Autores"], status_code=status.HTTP_200_OK)
async def get_autor_by_id(id_autor: int):
    """
    Obtiene un autor por su ID.
    """
    return await get_autor(id_autor)

@router.delete("/{id_autor}",tags=["Autores"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_autor_by_id(id_autor: int):
    """
    Elimina un autor por su ID.
    """
    return await delete_autor(id_autor)

@router.post("",tags=["Autores"], status_code=status.HTTP_201_CREATED)
async def post_autor(autor: AutorCreate):
    """
    Crea un nuevo autor en la base de datos.
    """
    return await create_autor(autor)

@router.get("/{id_autor}/comics",tags=["Autores"], status_code=status.HTTP_200_OK)
async def get_autor_comics_by_id(id_autor: int):
    """
    Obtiene todos los cómics de un autor.

    """
    return await get_autor_comics(id_autor)