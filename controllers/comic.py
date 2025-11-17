import json
from fastapi import HTTPException
from utils.database import execute_query_json
from models.comic import Comic, ComicUpdate

async def get_all_comics():
    selectscript = """SELECT 
    c.id_comic,
    c.num_comic,
    c.titulo,
    c.fecha_publicacion,
    e.id_editorial,
    e.nombre AS nombre_editorial
FROM comicverse.comic c
INNER JOIN comicverse.editorial e 
    ON c.id_editorial = e.id_editorial
"""
    try:
        result = await execute_query_json(selectscript)
        result_dict = json.loads(result)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def create_comic(comic: Comic):
    sql_insert = """
        INSERT INTO comicverse.comic (num_comic, titulo, id_editorial, id_autor, fecha_publicacion, inventario)
        OUTPUT INSERTED.id_comic
        VALUES (?, ?, ?, ?, ?, ?);
    """
    params = [
        comic.num_comic,
        comic.titulo,
        comic.id_editorial,
        comic.id_autor,
        comic.fecha_publicacion,
        comic.inventario
    ]

    try:
        result = await execute_query_json(sql_insert, params, needs_commit=True)
        result_dict = json.loads(result) if isinstance(result, str) else result
        id_comic = result_dict[0]["id_comic"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al insertar cómic: {str(e)}")

    sql_select = """
        SELECT [id_comic], [num_comic], [titulo], [id_editorial], [id_autor], [fecha_publicacion], [inventario]
        FROM comicverse.comic
        WHERE id_comic = ?;
    """
    try:
        result = await execute_query_json(sql_select, [id_comic])
        result_dict = json.loads(result) if isinstance(result, str) else result
        return result_dict[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar cómic: {str(e)}")

async def update_comic(id_comic: int, comic: ComicUpdate):
    # 1. Obtener inventario actual
    sql_get = "SELECT inventario FROM comicverse.comic WHERE id_comic = ?;"
    try:
        result = await execute_query_json(sql_get, [id_comic])
        result_dict = json.loads(result) if isinstance(result, str) else result

        if not result_dict:
            raise HTTPException(status_code=404, detail="Comic no encontrado")

        inventario_actual = result_dict[0]["inventario"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar inventario: {str(e)}")

    # 2. Calcular nuevo inventario
    nuevo_inventario = inventario_actual + (comic.inventario or 0)

    # 3. Construir dinámicamente el UPDATE
    dict_comic = comic.model_dump(exclude_none=True)
    if "inventario" in dict_comic:
        dict_comic["inventario"] = nuevo_inventario

    keys = [k for k in dict_comic.keys()]
    variables = " = ?, ".join(keys) + " = ?"

    sql_update = f"""
        UPDATE comicverse.comic
        SET {variables}
        WHERE id_comic = ?;
    """

    params = [dict_comic[v] for v in keys]
    params.append(id_comic)

    try:
        await execute_query_json(sql_update, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar comic: {str(e)}")

    # 4. Consultar comic actualizado
    sqlfind = """
        SELECT [id_comic], [num_comic], [titulo], [id_editorial], [id_autor], [fecha_publicacion], [inventario]
        FROM comicverse.comic
        WHERE id_comic = ?;
    """
    try:
        result = await execute_query_json(sqlfind, [id_comic])
        result_dict = json.loads(result)

        if len(result_dict) > 0:
            return result_dict[0]
        else:
            raise HTTPException(status_code=404, detail="Error al consultar comic actualizado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar comic: {str(e)}")
    
async def delete_comic(id_comic: int):
    # 1. Verificar si el cómic existe
    sql_check = "SELECT id_comic FROM comicverse.comic WHERE id_comic = ?;"
    result = await execute_query_json(sql_check, [id_comic])
    comic = json.loads(result) if isinstance(result, str) else result

    if not comic:
        raise HTTPException(status_code=404, detail="Cómic no encontrado")

    # 2. Verificar si está asociado a pedidos
    sql_check_pedidos = """
        SELECT COUNT(*) AS total
        FROM comicverse.comics_pedidos
        WHERE id_comic = ?;
    """
    result_pedidos = await execute_query_json(sql_check_pedidos, [id_comic])
    pedidos = json.loads(result_pedidos) if isinstance(result_pedidos, str) else result_pedidos

    if pedidos[0]["total"] > 0:
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar el cómic porque está asociado a pedidos"
        )

    # 3. Eliminar el cómic
    sql_delete = "DELETE FROM comicverse.comic WHERE id_comic = ?;"
    try:
        await execute_query_json(sql_delete, [id_comic], needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar cómic: {str(e)}")

async def get_comic(id_comic: int):
    sql = """
        SELECT 
            c.id_comic,
            c.num_comic,
            c.titulo,
            c.fecha_publicacion,
            c.inventario,
            e.id_editorial,
            e.nombre AS nombre_editorial,
            e.sitio_web AS sitio_web_editorial,
            a.id_autor,
            a.nombre AS nombre_autor,
            a.apellido AS apellido_autor,
            a.email AS email_autor
        FROM comicverse.comic c
        INNER JOIN comicverse.editorial e ON c.id_editorial = e.id_editorial
        INNER JOIN comicverse.autor a ON c.id_autor = a.id_autor
        WHERE c.id_comic = ?;
    """
    try:
        result = await execute_query_json(sql, [id_comic])
        comic = json.loads(result) if isinstance(result, str) else result

        return comic[0]
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Cómic no encontrado: {str(e)}")

async def get_comic_pedidos(id_comic: int):
    sql = """
        SELECT 
            p.id_pedido,
            p.fecha_pedido,
            p.fecha_entrega,
            p.id_cliente,
            cl.nombre AS nombre_cliente,
            cl.apellido AS apellido_cliente,
            cl.email AS email_cliente,
            cp.id_comic,
            c.titulo AS titulo_comic,
            cp.cantidad_comics,
            cp.estado
        FROM comicverse.pedido p
        INNER JOIN comicverse.comics_pedidos cp ON p.id_pedido = cp.id_pedido
        INNER JOIN comicverse.comic c ON cp.id_comic = c.id_comic
        INNER JOIN comicverse.cliente cl ON p.id_cliente = cl.id_cliente
        WHERE cp.id_comic = ?;
    """
    try:
        result = await execute_query_json(sql, [id_comic])
        pedidos = json.loads(result) if isinstance(result, str) else result

        if not pedidos:
            raise HTTPException(status_code=404, detail="No hay pedidos asociados a este cómic")

        return {
            "id_comic": id_comic,
            "pedidos": pedidos
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar pedidos del cómic: {str(e)}")
    
