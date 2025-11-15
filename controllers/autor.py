import json
from fastapi import HTTPException
from utils.database import execute_query_json

async def get_all_autores():
    selectscript = """
        SELECT [id_autor], [nombre], [apellido], [email]
        FROM [comicverse].[autor]
    """
    try:
        result = await execute_query_json(selectscript)
        result_dict = json.loads(result)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
