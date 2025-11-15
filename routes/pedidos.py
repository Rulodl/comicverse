from fastapi import APIRouter, HTTPException, status
from models.pedido import PedidoCreate   # importamos el modelo que definimos
from controllers.pedidos import create_pedido, get_all_pedidos   # función en controllers que maneja la inserción

router = APIRouter(prefix="/pedidos")

from fastapi import APIRouter, status, HTTPException
from controllers.pedidos import get_all_pedidos

router = APIRouter(prefix="/pedidos")

@router.get("/", tags=["Pedidos"], status_code=status.HTTP_200_OK)
async def get_all():
    """
    Devuelve todos los pedidos registrados en la base de datos.
    """
    try:
        result = await get_all_pedidos()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener pedidos: {str(e)}")


@router.post("/", tags=["Pedidos"], status_code=status.HTTP_201_CREATED)
async def post_pedido(pedido: PedidoCreate):
    """
    Endpoint para crear un nuevo pedido con sus cómics asociados.
    - Inserta cabecera en la tabla pedido.
    - Inserta detalle en comics_pedidos.
    - El trigger en DB valida inventario y descuenta stock automáticamente.
    """
    try:
        nuevo_pedido = await create_pedido(pedido)
        return nuevo_pedido
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear pedido: {str(e)}")
