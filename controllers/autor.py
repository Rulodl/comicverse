import json
from fastapi import HTTPException
from utils.database import execute_query_json
from models.autor import AutorUpdate, AutorCreate

async def get_all_autores():
    selectscript = """
        SELECT [id_autor], [nombre], [apellido]
        FROM [comicverse].[autor]
    """
    try:
        result = await execute_query_json(selectscript)
        result_dict = json.loads(result)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def update_autor(id_autor: int, autor: AutorUpdate):
    dict_autor = autor.model_dump(exclude_none=True)

    if not dict_autor:
        raise HTTPException(status_code=400, detail="No se enviaron campos para actualizar")

    keys = [k for k in dict_autor.keys()]
    variables = " = ?, ".join(keys) + " = ?"

    sql_update = f"""
        UPDATE comicverse.autor
        SET {variables}
        WHERE id_autor = ?;
    """

    params = [dict_autor[v] for v in keys]
    params.append(id_autor)

    try:
        await execute_query_json(sql_update, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar autor: {str(e)}")

    sqlfind = """
        SELECT [id_autor], [nombre], [apellido], [email]
        FROM comicverse.autor
        WHERE id_autor = ?;
    """
    try:
        result = await execute_query_json(sqlfind, [id_autor])
        result_dict = json.loads(result)

        if len(result_dict) > 0:
            return result_dict[0]
        else:
            raise HTTPException(status_code=404, detail="Error al consultar autor actualizado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar autor: {str(e)}")
    
async def get_autor(id_autor: int):
    sql = """
        SELECT 
            a.id_autor,
            a.nombre,
            a.apellido,
            a.email,
            COUNT(c.id_comic) AS num_comics
        FROM comicverse.autor a
        LEFT JOIN comicverse.comic c ON a.id_autor = c.id_autor
        WHERE a.id_autor = ?
        GROUP BY a.id_autor, a.nombre, a.apellido, a.email;
    """
    try:
        result = await execute_query_json(sql, [id_autor])
        autor = json.loads(result) if isinstance(result, str) else result

        if not autor:
            raise HTTPException(status_code=404, detail="Autor no encontrado")

        return autor[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar autor: {str(e)}")

async def delete_autor(id_autor: int):

    sql_check = "SELECT id_autor FROM comicverse.autor WHERE id_autor = ?;"
    result = await execute_query_json(sql_check, [id_autor])
    autor = json.loads(result) if isinstance(result, str) else result

    if not autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado")

    sql_check_comics = "SELECT COUNT(*) AS total FROM comicverse.comic WHERE id_autor = ?;"
    result_comics = await execute_query_json(sql_check_comics, [id_autor])
    comics = json.loads(result_comics) if isinstance(result_comics, str) else result_comics

    if comics[0]["total"] > 0:
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar el autor porque está asociado a cómics"
        )
    sql_delete = "DELETE FROM comicverse.autor WHERE id_autor = ?;"
    await execute_query_json(sql_delete, [id_autor], needs_commit=True)

    return {"message": f"Autor {id_autor} eliminado correctamente"}

async def create_autor(autor: AutorCreate):
    sql_insert = """
        INSERT INTO comicverse.autor (nombre, apellido, email)
        OUTPUT INSERTED.id_autor
        VALUES (?, ?, ?);
    """
    params = [autor.nombre, autor.apellido, autor.email]

    try:
        result = await execute_query_json(sql_insert, params, needs_commit=True)
        result_dict = json.loads(result) if isinstance(result, str) else result
        id_autor = result_dict[0]["id_autor"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al insertar autor: {str(e)}")

    sql_select = """
        SELECT id_autor, nombre, apellido, email
        FROM comicverse.autor
        WHERE id_autor = ?;
    """
    try:
        result = await execute_query_json(sql_select, [id_autor])
        result_dict = json.loads(result) if isinstance(result, str) else result
        return result_dict[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar autor: {str(e)}")

async def get_autor_comics(id_autor: int):
    sql = """
        SELECT 
            a.id_autor,
            a.nombre AS nombre_autor,
            a.apellido AS apellido_autor,
            c.id_comic,
            c.titulo
        FROM comicverse.autor a
        LEFT JOIN comicverse.comic c ON a.id_autor = c.id_autor
        WHERE a.id_autor = ?;
    """
    try:
        result = await execute_query_json(sql, [id_autor])
        rows = json.loads(result) if isinstance(result, str) else result

        if not rows:
            raise HTTPException(status_code=404, detail="Autor no encontrado")

        autor_info = {
            "id_autor": rows[0]["id_autor"],
            "nombre_autor": rows[0]["nombre_autor"],
            "apellido_autor": rows[0]["apellido_autor"]
        }

        comics = [
            {"id_comic": r["id_comic"], "titulo": r["titulo"]}
            for r in rows if r["id_comic"] is not None
        ]

        return {
            **autor_info,
            "total_comics": len(comics),
            "comics": comics
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar cómics del autor: {str(e)}")
