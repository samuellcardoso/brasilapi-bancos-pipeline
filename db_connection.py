import os
import psycopg
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    """Abre uma conexao somente quando a etapa de carga e executada."""
    return psycopg.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
    )
