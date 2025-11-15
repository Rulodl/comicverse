import json
from fastapi import HTTPException
from utils.database import execute_query_json

async def get_all_comics():
    selectscript = """
        SELECT [id_comic],
            [num_comic],
            [titulo],
            [id_editorial],
            [id_autor],
            [fecha_publicacion],
            [inventario]
        FROM [comicverse].[comic]
    """
    try:
        result = await execute_query_json(selectscript)
        result_dict = json.loads(result)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
