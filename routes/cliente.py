from fastapi import APIRouter, status, HTTPException
from models.cliente import Cliente, ClienteUpdate
from controllers.cliente import (get_all_clientes, 
                                create_cliente, 
                                get_cliente, 
                                delete_cliente, 
                                update_cliente, 
                                get_cliente_pedidos
                                )

router = APIRouter(prefix="/clientes")

@router.get("", tags=["Clientes"], status_code=status.HTTP_200_OK)
async def get_all():
    """
    Devuelve todos los clientes registrados en la base de datos.
    """
    result = await get_all_clientes()
    return result

@router.get("/{id_cliente}", tags=["Clientes"], status_code=status.HTTP_200_OK)
async def get_one_cliente(id_cliente: int):
    """
    Devuelve un cliente específico por su ID.
    """
    try:
        result = await get_cliente(id_cliente)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener cliente: {str(e)}")

@router.post("", tags=["Clientes"], status_code=status.HTTP_201_CREATED)
async def post_cliente(cliente: Cliente):
    """
    Crea un nuevo cliente en la base de datos.
    """
    try:
        result = await create_cliente(cliente)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear cliente: {str(e)}")

@router.delete("/{id_cliente}", tags=["Clientes"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_one_cliente(id_cliente: int):
    """
    Elimina un cliente específico por su ID.
    """
    try:
        result = await delete_cliente(id_cliente)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar cliente: {str(e)}")

@router.put("/{id_cliente}", tags=["Clientes"], status_code=status.HTTP_200_OK)
async def put_cliente(id_cliente: int, cliente: ClienteUpdate):
    """
    Actualiza los datos de un cliente existente.
    """
    return await update_cliente(id_cliente, cliente)

@router.get("/{id_cliente}/pedidos",tags=["Clientes"], status_code=status.HTTP_200_OK)
async def get_cliente_pedidos_by_id(id_cliente: int):
    """
    Obtiene todos los pedidos realizados por un cliente.
    """
    return await get_cliente_pedidos(id_cliente)