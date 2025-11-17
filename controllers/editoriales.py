import json
import logging
from utils.database import execute_query_json
from models.editorial import Editorial, EditorialUpdate
from fastapi import HTTPException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_editorial(editorial: Editorial) -> dict:
    # 1. Insertar nueva editorial
    sql_insert = """
        INSERT INTO comicverse.editorial (nombre, fecha_fundacion, sitio_web)
        VALUES (?, ?, ?);
    """
    insert_params = [
        editorial.nombre,
        editorial.fecha_fundacion,
        editorial.sitio_web
    ]

    try:
        await execute_query_json(sql_insert, insert_params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al insertar editorial: {str(e)}")

    # 2. Consultar editorial recién insertada por nombre
    sql_select = """
        SELECT id_editorial, nombre, fecha_fundacion, sitio_web
        FROM comicverse.editorial
        WHERE nombre = ?;
    """
    select_params = [editorial.nombre]

    try:
        result = await execute_query_json(sql_select, params=select_params)
        result_dict = json.loads(result) if isinstance(result, str) else result

        if len(result_dict) > 0:
            return result_dict[0]
        else:
            raise HTTPException(status_code=404, detail="Editorial no encontrada después de insertar")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar editorial: {str(e)}")

async def get_all_editoriales() -> list[Editorial]:

    selectscript = """
        SELECT [id_editorial]
        ,[nombre]
        FROM [comicverse].[editorial]
    """

    result_dict=[]
    try:
        result = await execute_query_json(selectscript)
        result_dict = json.loads(result)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")
    
async def get_one_editorial(id_editorial: int):
    sql_select = """
        SELECT e.id_editorial,
            e.nombre,
            e.fecha_fundacion,
            e.sitio_web,
            COUNT(c.id_comic) AS total_comics
        FROM comicverse.editorial e
        LEFT JOIN comicverse.comic c
            ON e.id_editorial = c.id_editorial
        WHERE e.id_editorial = ?
        GROUP BY e.id_editorial, e.nombre, e.fecha_fundacion, e.sitio_web;
    """
    params = [id_editorial]

    try:
        result = await execute_query_json(sql_select, params=params)
        result_dict = json.loads(result) if isinstance(result, str) else result

        if len(result_dict) > 0:
            return result_dict[0]
        else:
            raise HTTPException(status_code=404, detail="Editorial not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def update_editorial(id_editorial: int, editorial: EditorialUpdate):
    dict_editorial = editorial.model_dump(exclude_none=True)

    if not dict_editorial:
        raise HTTPException(status_code=400, detail="No se enviaron campos para actualizar")

    # Construimos dinámicamente el UPDATE
    keys = [k for k in dict_editorial.keys()]
    variables = " = ?, ".join(keys) + " = ?"

    sql_update = f"""
        UPDATE comicverse.editorial
        SET {variables}
        WHERE id_editorial = ?;
    """

    params = [dict_editorial[v] for v in keys]
    params.append(id_editorial)

    try:
        await execute_query_json(sql_update, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar editorial: {str(e)}")

    # Consultamos la editorial actualizada
    sqlfind = """
        SELECT [id_editorial], [nombre], [fecha_fundacion], [sitio_web]
        FROM comicverse.editorial
        WHERE id_editorial = ?;
    """
    try:
        result = await execute_query_json(sqlfind, [id_editorial])
        result_dict = json.loads(result)

        if len(result_dict) > 0:
            return result_dict[0]
        else:
            raise HTTPException(status_code=404, detail="Error al consultar editorial actualizada")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar editorial: {str(e)}")

async def delete_editorial(id_editorial: int):
    # 1. Verificar si la editorial existe
    sql_check = "SELECT id_editorial FROM comicverse.editorial WHERE id_editorial = ?;"
    result = await execute_query_json(sql_check, [id_editorial])
    editorial = json.loads(result) if isinstance(result, str) else result

    if not editorial:
        raise HTTPException(status_code=404, detail="Editorial no encontrada")

    # 2. Verificar si tiene cómics asociados
    sql_check_comics = "SELECT COUNT(*) AS total FROM comicverse.comic WHERE id_editorial = ?;"
    result_comics = await execute_query_json(sql_check_comics, [id_editorial])
    comics = json.loads(result_comics) if isinstance(result_comics, str) else result_comics

    if comics[0]["total"] > 0:
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar la editorial porque tiene cómics asociados"
        )

    # 3. Eliminar la editorial
    sql_delete = "DELETE FROM comicverse.editorial WHERE id_editorial = ?;"
    await execute_query_json(sql_delete, [id_editorial], needs_commit=True)

    return {"message": f"Editorial {id_editorial} eliminada correctamente"}

async def get_editorial(id_editorial: int):
    # 1. Obtener datos de la editorial
    sql_editorial = """
        SELECT id_editorial, nombre, fecha_fundacion, sitio_web
        FROM comicverse.editorial
        WHERE id_editorial = ?;
    """
    result = await execute_query_json(sql_editorial, [id_editorial])
    editorial = json.loads(result) if isinstance(result, str) else result

    if not editorial:
        raise HTTPException(status_code=404, detail="Editorial no encontrada")

    # 2. Contar cómics asociados
    sql_count_comics = """
        SELECT COUNT(*) AS cantidad_comics
        FROM comicverse.comic
        WHERE id_editorial = ?;
    """
    result_comics = await execute_query_json(sql_count_comics, [id_editorial])
    comics = json.loads(result_comics) if isinstance(result_comics, str) else result_comics
    cantidad = comics[0]["cantidad_comics"]

    # 3. Armar respuesta
    return {
        "id_editorial": editorial[0]["id_editorial"],
        "nombre": editorial[0]["nombre"],
        "fecha_fundacion": editorial[0]["fecha_fundacion"],
        "sitio_web": editorial[0]["sitio_web"],
        "cantidad_comics": cantidad
    }

async def get_editorial_comics(id_editorial: int):
    # 1. Verificar si la editorial existe
    sql_check = """
        SELECT id_editorial, nombre
        FROM comicverse.editorial
        WHERE id_editorial = ?;
    """
    result = await execute_query_json(sql_check, [id_editorial])
    editorial = json.loads(result) if isinstance(result, str) else result

    if not editorial:
        raise HTTPException(status_code=404, detail="Editorial no encontrada")

    # 2. Obtener cómics asociados (sin inventario)
    sql_comics = """
        SELECT 
            c.id_comic,
            c.num_comic,
            c.titulo,
            c.fecha_publicacion
        FROM comicverse.comic c
        WHERE c.id_editorial = ?;
    """
    result_comics = await execute_query_json(sql_comics, [id_editorial])
    comics = json.loads(result_comics) if isinstance(result_comics, str) else result_comics

    # 3. Armar respuesta
    return {
        "id_editorial": editorial[0]["id_editorial"],
        "nombre_editorial": editorial[0]["nombre"],
        "cantidad_comics": len(comics),
        "comics": comics
    }

async def get_editorial_comic(id_editorial: int, id_comic: int):
    # 1. Verificar si la editorial existe
    sql_check_editorial = """
        SELECT id_editorial, nombre
        FROM comicverse.editorial
        WHERE id_editorial = ?;
    """
    result_editorial = await execute_query_json(sql_check_editorial, [id_editorial])
    editorial = json.loads(result_editorial) if isinstance(result_editorial, str) else result_editorial

    if not editorial:
        raise HTTPException(status_code=404, detail="Editorial no encontrada")

    # 2. Obtener cómic con join al autor
    sql_comic = """
        SELECT 
            c.id_comic,
            c.num_comic,
            c.titulo,
            c.fecha_publicacion,
            c.inventario,
            a.id_autor,
            a.nombre AS nombre_autor,
            a.apellido AS apellido_autor,
            e.id_editorial,
            e.nombre AS nombre_editorial
        FROM comicverse.comic c
        INNER JOIN comicverse.autor a ON c.id_autor = a.id_autor
        INNER JOIN comicverse.editorial e ON c.id_editorial = e.id_editorial
        WHERE c.id_editorial = ? AND c.id_comic = ?;
    """
    result_comic = await execute_query_json(sql_comic, [id_editorial, id_comic])
    comic = json.loads(result_comic) if isinstance(result_comic, str) else result_comic

    if not comic:
        raise HTTPException(status_code=404, detail="Cómic no encontrado en esta editorial")

    # 3. Devolver directamente el cómic con datos de editorial y autor
    return comic[0]

















