# utils/database.py
from dotenv import load_dotenv
import os
import pyodbc
import logging
import json

# Carga .env (si necesitas ruta explícita: load_dotenv("ruta/.env"))
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Variables de entorno
driver = os.getenv("SQL_DRIVER") or "ODBC Driver 17 for SQL Server"
server = os.getenv("SQL_SERVER")
database = os.getenv("SQL_DATABASE")
username = os.getenv("SQL_USERNAME")
password = os.getenv("SQL_PASSWORD")
trusted = os.getenv("SQL_TRUSTED", "false").lower() in ("1", "true", "yes")
port = os.getenv("SQL_PORT", "1433")

# Log para diagnosticar (no muestra contraseña)
logger.info(f"DB loaded: server={server}:{port}, db={database}, username-set={bool(username)}, trusted={trusted}")

# ---------------------------------------------------------------------
# 1) Construcción segura del connection string (evita UID=None)
# ---------------------------------------------------------------------
def _build_connection_string():
    if not server or not database:
        raise RuntimeError("Faltan SQL_SERVER o SQL_DATABASE en .env")

    if trusted:
        # Windows Authentication
        return (
            f"DRIVER={{{driver}}};"
            f"SERVER={server},{port};"
            f"DATABASE={database};"
            "Trusted_Connection=yes;"
            "TrustServerCertificate=yes;"
        )

    # SQL Authentication: user/pass obligatorios
    if not username:
        raise RuntimeError("Falta SQL_USERNAME en .env")
    if not password:
        raise RuntimeError("Falta SQL_PASSWORD en .env")

    return (
        f"DRIVER={{{driver}}};"
        f"SERVER={server},{port};"
        f"DATABASE={database};"
        f"UID={username};PWD={password};"
        "TrustServerCertificate=yes;"
    )

# ---------------------------------------------------------------------
# 2) Conexión a la base de datos
# ---------------------------------------------------------------------
async def get_db_connection():
    conn_str = _build_connection_string()

    logger.info("Intentando conectar a la base de datos...")
    try:
        conn = pyodbc.connect(conn_str, timeout=10)
        logger.info("Conexión exitosa a la base de datos.")
        return conn
    except pyodbc.Error as e:
        logger.error(f"Error de conexión a la base de datos: {str(e)}")
        raise Exception(f"Error de conexión a la base de datos: {str(e)}")
    except Exception as e:
        logger.error(f"Error inesperado durante la conexión: {str(e)}")
        raise

# ---------------------------------------------------------------------
# 3) TU MISMO execute_query_json, tal cual estaba
# ---------------------------------------------------------------------
async def execute_query_json(sql_template, params=None, needs_commit=False):

    conn = None
    cursor = None
    try:
        conn = await get_db_connection()
        cursor = conn.cursor()

        param_info = "(sin parámetros)" if not params else f"(con {len(params)} parámetros)"
        logger.info(f"Ejecutando consulta {param_info}: {sql_template}")

        if params:
            cursor.execute(sql_template, params)
        else:
            cursor.execute(sql_template)

        results = []
        if cursor.description:
            columns = [column[0] for column in cursor.description]
            logger.info(f"Columnas obtenidas: {columns}")

            for row in cursor.fetchall():
                processed_row = [
                    str(item) if isinstance(item, (bytes, bytearray)) else item
                    for item in row
                ]
                results.append(dict(zip(columns, processed_row)))
        else:
            logger.info("La consulta no devolvió columnas (posible INSERT/UPDATE/DELETE).")

        if needs_commit:
            logger.info("Realizando commit de la transacción.")
            conn.commit()

        # ← regresamos EXACTAMENTE como lo tenías: JSON string
        return json.dumps(results, default=str)

    except pyodbc.Error as e:
        logger.error(f"Error ejecutando la consulta (SQLSTATE: {e.args[0]}): {str(e)}")

        if conn and needs_commit:
            try:
                logger.warning("Realizando rollback debido a error.")
                conn.rollback()
            except pyodbc.Error as rb_e:
                logger.error(f"Error durante el rollback: {rb_e}")

        raise Exception(f"Error ejecutando consulta: {str(e)}") from e

    except Exception as e:
        logger.error(f"Error inesperado durante ejecución de la consulta: {str(e)}")
        raise

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            logger.info("Conexión cerrada.")
