from fastapi import HTTPException
import json
from utils.database import execute_query_json
from models.cliente import Cliente
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
