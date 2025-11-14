from fastapi import APIRouter, HTTPException, Request
from models.editorial import Editorial
from controllers.editoriales import create_editorial

router = APIRouter(prefix="/editoriales")

@router.post("/", tags=["Editoriales"])
async def create_new_editorial(editorial_data: Editorial):
    result = await create_editorial(editorial_data)

    return result
        