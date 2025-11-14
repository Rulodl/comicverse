import json
import logging
from utils.database import execute_query_json
from models.editorial import Editorial
from fastapi import HTTPException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_editorial(editorial: Editorial) -> Editorial:
    sqlscript = """
    INSERT INTO comicverse.editorial (nombre, fecha_fundacion, sitio_web)
    VALUES (?, ?, ?);
    """
    params = [
        editorial.nombre,
        editorial.fecha_fundacion,
        editorial.sitio_web
    ]

    insert_result = None
    try:
        insert_result = await execute_query_json(sqlscript, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"database error:{str(e)}")
    
    
    sqlfind = """
        SELECT [id_editorial]
        ,[nombre]
        ,[fecha_fundacion]
        ,[sitio_web]
        FROM [comicverse].[editorial]
    WHERE nombre = ?;  
    """
    params_find = [editorial.nombre]
    result_dict = []
    try:
        result = await execute_query_json(sqlscript, params=params)
        if len(result) > 0:
            return result_dict[0]
        else:
            return  []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"database error:{str(e)}")
    