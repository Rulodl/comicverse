import json
from utils.database import execute_query_json
from fastapi import HTTPException
from datetime import datetime, date
from models.pedido import  ComicReplace, PedidoEstadoUpdate

async def create_pedido(pedido):

    sql_insert_pedido = """
        INSERT INTO comicverse.pedido (id_cliente, fecha_pedido, fecha_entrega)
        OUTPUT INSERTED.id_pedido
        VALUES (?, ?, ?);
    """
    params_pedido = [
        pedido.id_cliente,
        datetime.now(),         
        pedido.fecha_entrega   
    ]

    try:
        result = await execute_query_json(sql_insert_pedido, params_pedido, needs_commit=True)
        result_dict = json.loads(result) if isinstance(result, str) else result
        id_pedido = result_dict[0]["id_pedido"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al insertar pedido: {str(e)}")

    sql_insert_detalle = """
        INSERT INTO comicverse.comics_pedidos (id_pedido, id_comic, cantidad_comics, estado)
        VALUES (?, ?, ?, 'Pendiente');
    """
    try:
        for comic in pedido.comics:
            await execute_query_json(
                sql_insert_detalle,
                [id_pedido, comic.id_comic, comic.cantidad_comics],
                needs_commit=True
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al insertar detalle de cómics: {str(e)}")

    #Devolver pedido 
    sql_select = """
        SELECT p.id_pedido, p.id_cliente, p.fecha_pedido, p.fecha_entrega,
            cp.id_comic, c.titulo, cp.cantidad_comics, cp.estado
        FROM comicverse.pedido p
        INNER JOIN comicverse.comics_pedidos cp ON p.id_pedido = cp.id_pedido
        INNER JOIN comicverse.comic c ON cp.id_comic = c.id_comic
        WHERE p.id_pedido = ?;
    """
    try:
        result = await execute_query_json(sql_select, [id_pedido])
        rows = json.loads(result) if isinstance(result, str) else result

        if not rows:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")

        pedido_info = {
            "id_pedido": rows[0]["id_pedido"],
            "id_cliente": rows[0]["id_cliente"],
            "fecha_pedido": rows[0]["fecha_pedido"],
            "fecha_entrega": rows[0]["fecha_entrega"],
            "comics": [
                {
                    "id_comic": r["id_comic"],
                    "titulo": r["titulo"],
                    "cantidad_comics": r["cantidad_comics"],
                    "estado": r["estado"]
                }
                for r in rows
            ]
        }

        return pedido_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar pedido: {str(e)}")

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

async def get_pedido(id_pedido: int):
    sql = """
        SELECT 
            p.id_pedido,
            p.id_cliente,
            p.fecha_pedido,
            p.fecha_entrega,
            c.nombre AS nombre_cliente,
            c.apellido AS apellido_cliente,
            cp.id_comic,
            co.titulo AS titulo_comic,
            cp.cantidad_comics,
            cp.estado
        FROM comicverse.pedido p
        INNER JOIN comicverse.cliente c ON p.id_cliente = c.id_cliente
        INNER JOIN comicverse.comics_pedidos cp ON p.id_pedido = cp.id_pedido
        INNER JOIN comicverse.comic co ON cp.id_comic = co.id_comic
        WHERE p.id_pedido = ?;
    """
    try:
        result = await execute_query_json(sql, [id_pedido])
        rows = json.loads(result) if isinstance(result, str) else result

        if not rows:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")

        pedido_info = {
            "id_pedido": rows[0]["id_pedido"],
            "id_cliente": rows[0]["id_cliente"],
            "nombre_cliente": rows[0]["nombre_cliente"],
            "apellido_cliente": rows[0]["apellido_cliente"],
            "fecha_pedido": rows[0]["fecha_pedido"],
            "fecha_entrega": rows[0]["fecha_entrega"],
            "comics": [
                {
                    "id_comic": r["id_comic"],
                    "titulo_comic": r["titulo_comic"],
                    "cantidad_comics": r["cantidad_comics"],
                    "estado": r["estado"]
                }
                for r in rows
            ]
        }

        return pedido_info

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado al consultar pedido: {str(e)}")

async def update_pedido_estado(id_pedido: int, pedido: PedidoEstadoUpdate):

    if pedido.fecha_entrega is not None:
        fecha_str = (
            pedido.fecha_entrega.isoformat()
            if isinstance(pedido.fecha_entrega, date)
            else str(pedido.fecha_entrega)
        )
        sql_update_pedido = """
            UPDATE comicverse.pedido
            SET fecha_entrega = ?
            WHERE id_pedido = ?;
        """
        await execute_query_json(sql_update_pedido, [fecha_str, id_pedido], needs_commit=True)


    if pedido.comics:
        for item in pedido.comics:
            sql_check = """
                SELECT estado
                FROM comicverse.comics_pedidos
                WHERE id_pedido = ? AND id_comic = ?;
            """
            res_line = await execute_query_json(sql_check, [id_pedido, item.id_comic])
            line = json.loads(res_line) if isinstance(res_line, str) else res_line

            if not line:
                raise HTTPException(
                    status_code=404,
                    detail=f"La línea (id_pedido={id_pedido}, id_comic={item.id_comic}) no existe."
                )

            nuevo_estado = item.estado if item.estado is not None else line[0]["estado"]

            sql_update_line = """
                UPDATE comicverse.comics_pedidos
                SET estado = ?
                WHERE id_pedido = ? AND id_comic = ?;
            """
            await execute_query_json(sql_update_line, [nuevo_estado, id_pedido, item.id_comic], needs_commit=True)


    return await get_pedido(id_pedido)

async def replace_comic_in_pedido(id_pedido: int, id_comic: int, data: ComicReplace):

    sql_get_cantidad = """
        SELECT cantidad_comics
        FROM comicverse.comics_pedidos
        WHERE id_pedido = ? AND id_comic = ?;
    """
    result = await execute_query_json(sql_get_cantidad, [id_pedido, id_comic])
    result_dict = json.loads(result) if isinstance(result, str) else result
    cantidad_original = result_dict[0]["cantidad_comics"] if result_dict else 0


    sql_sumar_inventario = """
        UPDATE comicverse.comic
        SET inventario = inventario + ?
        WHERE id_comic = ?;
    """
    await execute_query_json(sql_sumar_inventario, [cantidad_original, id_comic], needs_commit=True)


    sql_delete = """
        DELETE FROM comicverse.comics_pedidos
        WHERE id_pedido = ? AND id_comic = ?;
    """
    await execute_query_json(sql_delete, [id_pedido, id_comic], needs_commit=True)

    sql_insert = """
        INSERT INTO comicverse.comics_pedidos (id_pedido, id_comic, cantidad_comics, estado)
        VALUES (?, ?, ?, ?);
    """
    await execute_query_json(sql_insert, [id_pedido, data.id_comic_nuevo, data.cantidad_comics, data.estado], needs_commit=True)

    return await get_pedido(id_pedido)

async def delete_pedido(id_pedido: int):

    sql_get_lineas = """
        SELECT id_comic, cantidad_comics
        FROM comicverse.comics_pedidos
        WHERE id_pedido = ?;
    """
    result = await execute_query_json(sql_get_lineas, [id_pedido])
    lineas = json.loads(result) if isinstance(result, str) else result

    if not lineas:
        raise HTTPException(status_code=404, detail="Pedido no encontrado o sin cómics")

    for linea in lineas:
        sql_update_inventario = """
            UPDATE comicverse.comic
            SET inventario = inventario + ?
            WHERE id_comic = ?;
        """
        await execute_query_json(sql_update_inventario, [linea["cantidad_comics"], linea["id_comic"]], needs_commit=True)

    sql_delete_lineas = """
        DELETE FROM comicverse.comics_pedidos
        WHERE id_pedido = ?;
    """
    await execute_query_json(sql_delete_lineas, [id_pedido], needs_commit=True)

    sql_delete_pedido = """
        DELETE FROM comicverse.pedido
        WHERE id_pedido = ?;
    """
    await execute_query_json(sql_delete_pedido, [id_pedido], needs_commit=True)

async def delete_comic_in_pedido(id_pedido: int, id_comic: int):

    sql_get_cantidad = """
        SELECT cantidad_comics
        FROM comicverse.comics_pedidos
        WHERE id_pedido = ? AND id_comic = ?;
    """
    result = await execute_query_json(sql_get_cantidad, [id_pedido, id_comic])
    result_dict = json.loads(result) if isinstance(result, str) else result

    if not result_dict:
        raise HTTPException(status_code=404, detail="La línea del pedido no existe")

    cantidad = result_dict[0]["cantidad_comics"]


    sql_update_inventario = """
        UPDATE comicverse.comic
        SET inventario = inventario + ?
        WHERE id_comic = ?;
    """
    try:
        await execute_query_json(sql_update_inventario, [cantidad, id_comic], needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al devolver inventario: {str(e)}")


    sql_delete = """
        DELETE FROM comicverse.comics_pedidos
        WHERE id_pedido = ? AND id_comic = ?;
    """
    try:
        await execute_query_json(sql_delete, [id_pedido, id_comic], needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar cómic del pedido: {str(e)}")


    return await get_pedido(id_pedido)


