import json
import logging
from utils.database import execute_query_json
from models.editorial import Editorial
from fastapi import HTTPException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_editorial(editorial: Editorial):
    sql_insert = """
        INSERT INTO [comicverse].[editorial] ([nombre], [fecha_fundacion], [sitio_web])
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
        # Manejo de error por duplicado en sitio_web (UNIQUE constraint)
        if "UNIQUE" in str(e):
            raise HTTPException(status_code=400, detail="Sitio web ya registrado")
        raise HTTPException(status_code=500, detail=f"Database error on insert: {str(e)}")

    sql_select = """
        SELECT [id_editorial], [nombre], [fecha_fundacion], [sitio_web]
        FROM [comicverse].[editorial]
        WHERE sitio_web = ?;
    """
    select_params = [editorial.sitio_web]

    try:
        result = await execute_query_json(sql_select, params=select_params)
        result_dict = json.loads(result) if isinstance(result, str) else result

        if len(result_dict) > 0:
            return result_dict[0]
        else:
            raise HTTPException(status_code=404, detail="Editorial not found after insert")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error on select: {str(e)}")
    
#función para obtener todas las editoriales    
async def get_all_editoriales() -> list[Editorial]:

    selectscript = """
        SELECT [id_editorial]
        ,[nombre]
        ,[fecha_fundacion]
        ,[sitio_web]
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






























