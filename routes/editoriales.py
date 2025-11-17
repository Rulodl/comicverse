from fastapi import APIRouter, HTTPException, Request, status
from models.editorial import Editorial, EditorialUpdate
from controllers.editoriales import (create_editorial, 
                                    get_all_editoriales, 
                                    update_editorial,
                                    delete_editorial,
                                    get_editorial,
                                    get_editorial_comics,
                                    get_editorial_comic
                                    )

router = APIRouter(prefix="/editoriales")

@router.get( "" , tags=["Editoriales"], status_code=status.HTTP_200_OK )
async def get_all():
    result = await get_all_editoriales()
    return result

@router.get("/{id_editorial}", tags=["Editoriales"], status_code=status.HTTP_200_OK)
async def get_editorial_by_id(id_editorial: int):
    """
    Obtiene una editorial por su id
    """
    return await get_editorial(id_editorial)

@router.post("", tags=["Editoriales"], status_code=status.HTTP_201_CREATED )
async def create_new_editorial(editorial_data: Editorial):
    """
    Crea una nueva editorial en la base de datos.
    """
    result = await create_editorial(editorial_data)

    return result

@router.put("/{id_editorial}", tags=["Editoriales"], status_code=status.HTTP_200_OK)
async def update_editorial_information(id_editorial: int, editorial_data: EditorialUpdate):
    """
    Actualiza una editorial existente en la base de datos.
    """
    try:
        result = await update_editorial(id_editorial, editorial_data)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar editorial: {str(e)}")

@router.delete("/{id_editorial}", tags=["Editoriales"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_editorial_by_id(id_editorial: int):
    """
    Elimina una editorial:
    """
    return await delete_editorial(id_editorial)

@router.get("/{id_editorial}/comics", tags=["Editoriales"], status_code=status.HTTP_200_OK)
async def get_editorial_comics_by_id(id_editorial: int):
    """
    Obtiene todos los cómics asociados a una editorial
    """
    return await get_editorial_comics(id_editorial)

@router.get("/{id_editorial}/comics/{id_comic}", tags=["Editoriales"], status_code=status.HTTP_200_OK)
async def get_editorial_comic_by_id(id_editorial: int, id_comic: int):
    """
    Obtiene un cómic específico de una editorial
    """
    return await get_editorial_comic(id_editorial, id_comic)
