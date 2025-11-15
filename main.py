from fastapi import FastAPI
from routes.editoriales import router as router_editoriales
from routes.pedidos import router as router_pedidos
from routes.cliente import router as router_clientes
from routes.autor import router as router_autores
from routes.comic import router as router_comics    
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde .env
load_dotenv()

app = FastAPI(
    title="Comicverse API",
    description="API para gestionar editoriales, cómics, pedidos y clientes",
    version="1.0.0"
)

# Registrar routers
app.include_router(router_editoriales)
app.include_router(router_pedidos)
app.include_router(router_clientes)
app.include_router(router_autores)
app.include_router(router_comics)

@app.get("/")
async def root():
    return {"message": "Bienvenido a Comicverse API"}
