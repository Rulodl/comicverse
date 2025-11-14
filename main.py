from fastapi import FastAPI
from routes.editoriales import router as router_editoriales
from dotenv import load_dotenv
import os

app = FastAPI()

app.include_router(router_editoriales)


@app.get("/")
def read_root():
    return {"Hello": "World"}




load_dotenv()  # Carga las variables de entorno desde el archivo .env
@app.on_event("startup")
def startup():
    import logging
    logging.getLogger("uvicorn").info("CWD: %s", os.getcwd())
    logging.getLogger("uvicorn").info("SQL_USERNAME: %s", bool(os.getenv("SQL_USERNAME")))
    logging.getLogger("uvicorn").info("SQL_TRUSTED: %s", os.getenv("SQL_TRUSTED"))