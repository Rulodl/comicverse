from fastapi import APIRouter, HTTPException, Request, status
from models.editorial import Editorial
from controllers.editoriales import create_editorial, get_all_editoriales

router = APIRouter(prefix="/editoriales")

@router.post("/", tags=["Editoriales"], status_code=status.HTTP_201_CREATED )
async def create_new_editorial(editorial_data: Editorial):
    result = await create_editorial(editorial_data)

    return result

@router.get( "/" , tags=["Editoriales"], status_code=status.HTTP_200_OK )
async def get_all():
    result = await get_all_editoriales()
    return result


