from fastapi import APIRouter, HTTPException, status
from models.pedido import PedidoEstadoUpdate, ComicReplace, PedidoCreate
from fastapi import APIRouter, status
from controllers.pedidos import (
    create_pedido, 
    get_all_pedidos, 
    get_pedido,
    replace_comic_in_pedido, 
    update_pedido_estado, 
    delete_pedido,
    delete_comic_in_pedido
    )

router = APIRouter(prefix="/pedidos")

router = APIRouter(prefix="/pedidos")

@router.get("", tags=["Pedidos"], status_code=status.HTTP_200_OK)
async def get_all():
    """
    Devuelve todos los pedidos registrados en la base de datos.
    """
    try:
        result = await get_all_pedidos()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener pedidos: {str(e)}")

@router.post("", tags=["Pedidos"], status_code=status.HTTP_201_CREATED)
async def post_pedido(pedido: PedidoCreate):
    """
    Crea un nuevo pedido en la base de datos.
    """
    try:
        nuevo_pedido = await create_pedido(pedido)
        return nuevo_pedido
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear pedido: {str(e)}")

@router.get("/{id_pedido}", tags=["Pedidos"], status_code=status.HTTP_200_OK)
async def get_pedido_information(id_pedido: int):
    """
    Devuelve la información de un pedido específico
    """
    try:
        result = await get_pedido(id_pedido)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar pedido: {str(e)}")

@router.put("/{id_pedido}", tags=["Pedidos"], status_code=status.HTTP_200_OK)
async def update_pedido_by_id(id_pedido: int, data: PedidoEstadoUpdate):
    """
    Actualiza un pedido existente
    """
    return await update_pedido_estado(id_pedido, data)

@router.put("/{id_pedido}/comics/{id_comic}", tags=["Pedidos"], status_code=status.HTTP_200_OK)
async def update_comic_in_pedido(id_pedido: int, id_comic: int, data: ComicReplace):
    """
    Reemplaza un cómic en un pedido existente
    """
    return await replace_comic_in_pedido(id_pedido, id_comic, data)

@router.delete("/{id_pedido}/comics/{id_comic}",tags=["Pedidos"], status_code=status.HTTP_200_OK)
async def delete_comic_from_pedido(id_pedido: int, id_comic: int):  
    """
    Elimina un cómic de un pedido
    """
    return await delete_comic_in_pedido(id_pedido, id_comic)

@router.delete("/{id_pedido}", tags=["Pedidos"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_pedido_by_id(id_pedido: int):
    """
    Elimina un pedido completo
    """
    return await delete_pedido(id_pedido)



