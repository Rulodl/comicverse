from fastapi import FastAPI
from routes.editoriales import router as router_editoriales
from routes.pedidos import router as router_pedidos
from routes.cliente import router as router_clientes
from routes.autor import router as router_autores
from routes.comic import router as router_comics    
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn

load_dotenv()

app = FastAPI(
    title="Comicverse API",
    description="API para gestionar editoriales, cómics, pedidos y clientes",
    version="1.0.0"
)

app.include_router(router_editoriales)
app.include_router(router_pedidos)
app.include_router(router_clientes)
app.include_router(router_autores)
app.include_router(router_comics)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")   
