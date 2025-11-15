import json
from utils.database import execute_query_json
from fastapi import HTTPException

async def create_pedido(pedido):
    # 1. Insertar cabecera del pedido
    sql_insert_pedido = """
        INSERT INTO comicverse.pedido (id_cliente, fecha_entrega)
        OUTPUT INSERTED.id_pedido
        VALUES (?, ?);
    """
    params_pedido = [pedido.cliente_id, pedido.fecha_entrega]

    result = await execute_query_json(sql_insert_pedido, params_pedido, needs_commit=True)
    result_dict = json.loads(result) if isinstance(result, str) else result
    id_pedido = result_dict[0]["id_pedido"]

    # 2. Insertar detalle de cómics
    sql_insert_detalle = """
        INSERT INTO comicverse.comics_pedidos (id_pedido, id_comic, cantidad_comics, estado)
        VALUES (?, ?, ?, 'Pendiente');
    """
    for comic in pedido.comics:
        await execute_query_json(sql_insert_detalle,
                                [id_pedido, comic.id_comic, comic.cantidad_comics],
                                needs_commit=True)

    # 3. Devolver pedido completo
    sql_select = """
        SELECT p.id_pedido, p.id_cliente, p.fecha_pedido, p.fecha_entrega,
            cp.id_comic, cp.cantidad_comics, cp.estado
        FROM comicverse.pedido p
        INNER JOIN comicverse.comics_pedidos cp ON p.id_pedido = cp.id_pedido
        WHERE p.id_pedido = ?;
    """
    result = await execute_query_json(sql_select, [id_pedido])
    result_dict = json.loads(result) if isinstance(result, str) else result

    return result_dict


import json
from fastapi import HTTPException
from utils.database import execute_query_json

async def get_all_pedidos():
    selectscript = """
        SELECT p.[id_pedido],
            p.[id_cliente],
            p.[fecha_pedido],
            p.[fecha_entrega],
            c.[nombre] AS nombre_cliente,
            c.[apellido] AS apellido_cliente
        FROM [comicverse].[pedido] AS p
        INNER JOIN [comicverse].[cliente] AS c
            ON p.[id_cliente] = c.[id_cliente]
    """
    try:
        result = await execute_query_json(selectscript)
        result_dict = json.loads(result)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
