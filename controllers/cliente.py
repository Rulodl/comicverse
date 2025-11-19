from fastapi import HTTPException
import json
from utils.database import execute_query_json
from models.cliente import Cliente, ClienteUpdate

from datetime import datetime

async def get_all_clientes() -> list[Cliente]:
    selectscript = """
        SELECT [id_cliente]
            ,[nombre]
            ,[apellido]
            ,[email]
        FROM [comicverse].[cliente]
    """

    result_dict = []
    try:
        result = await execute_query_json(selectscript)
        result_dict = json.loads(result)  
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def get_cliente(id_cliente: int):
    sql_select = """
        SELECT [id_cliente], [nombre], [apellido], [email], [fecha_creacion]
        FROM comicverse.cliente
        WHERE id_cliente = ?;
    """
    try:
        result = await execute_query_json(sql_select, [id_cliente])
        result_dict = json.loads(result) if isinstance(result, str) else result

        if len(result_dict) == 0:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")

        return result_dict[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar cliente: {str(e)}")

async def create_cliente(cliente: Cliente):

    sql_insert = """
        INSERT INTO comicverse.cliente (nombre, apellido, email, fecha_creacion)
        OUTPUT INSERTED.id_cliente
        VALUES (?, ?, ?, ?);
    """
    params = [
        cliente.nombre,
        cliente.apellido,
        cliente.email,
        datetime.now()
                    ]

    try:
        result = await execute_query_json(sql_insert, params, needs_commit=True)
        result_dict = json.loads(result) if isinstance(result, str) else result
        id_cliente = result_dict[0]["id_cliente"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al insertar cliente: {str(e)}")

    sql_select = """
        SELECT [id_cliente], [nombre], [apellido], [email], [fecha_creacion]
        FROM comicverse.cliente
        WHERE id_cliente = ?;
    """
    try:
        result = await execute_query_json(sql_select, [id_cliente])
        result_dict = json.loads(result) if isinstance(result, str) else result
        return result_dict[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar cliente: {str(e)}")

async def delete_cliente(id_cliente: int):

    sql_check = "SELECT id_cliente FROM comicverse.cliente WHERE id_cliente = ?;"
    result = await execute_query_json(sql_check, [id_cliente])
    cliente = json.loads(result) if isinstance(result, str) else result

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    sql_delete = "DELETE FROM comicverse.cliente WHERE id_cliente = ?;"
    try:
        await execute_query_json(sql_delete, [id_cliente], needs_commit=True)
        return {"message": f"Cliente con id {id_cliente} eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar cliente: {str(e)}")

async def update_cliente(id_cliente: int, cliente: ClienteUpdate) -> dict:

    dict_cliente = cliente.model_dump(exclude_none=True)

    keys = [k for k in dict_cliente.keys()]
    variables = " = ?, ".join(keys) + " = ?"

    updatescript = f"""
        UPDATE comicverse.cliente
        SET {variables}
        WHERE id_cliente = ?;
    """

    params = [dict_cliente[v] for v in keys]
    params.append(id_cliente)

    try:
        await execute_query_json(updatescript, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar cliente: {str(e)}")

    sqlfind = """
        SELECT id_cliente, nombre, apellido, email, fecha_creacion
        FROM comicverse.cliente
        WHERE id_cliente = ?;
    """
    try:
        result = await execute_query_json(sqlfind, [id_cliente])
        result_dict = json.loads(result) if isinstance(result, str) else result

        if len(result_dict) > 0:
            return result_dict[0]
        else:
            return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar cliente: {str(e)}")

async def get_cliente_pedidos(id_cliente: int):
    sql = """
        SELECT 
            p.id_pedido,
            p.fecha_pedido,
            p.fecha_entrega,
            p.total,
            cp.id_comic,
            c.titulo AS titulo_comic,
            cp.cantidad_comics,
            cp.estado
        FROM comicverse.pedido p
        INNER JOIN comicverse.comics_pedidos cp ON p.id_pedido = cp.id_pedido
        INNER JOIN comicverse.comic c ON cp.id_comic = c.id_comic
        WHERE p.id_cliente = ?;
    """
    try:
        result = await execute_query_json(sql, [id_cliente])
        pedidos = json.loads(result) if isinstance(result, str) else result

        if not pedidos:
            raise HTTPException(status_code=404)

        return {
            "id_cliente": id_cliente,
            "pedidos": pedidos
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"No se encontraron pedidos para este cliente: {str(e)}")


