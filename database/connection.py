import os
import mysql.connector
from sqlalchemy import create_engine, text

# Configuración de credenciales (lee las variables de Render o usa los valores locales por defecto)
usuario = os.getenv("DB_USER", "root")
password = os.getenv("DB_PASSWORD", "abril317")
host = os.getenv("DB_HOST", "localhost")
database = os.getenv("DB_NAME", "pangea_helpdesk_ia")

# 1. Engine de SQLAlchemy (para usuarios.py y otros módulos)
conexion_url = f"mysql+pymysql://{usuario}:{password}@{host}/{database}"
engine = create_engine(conexion_url)

# 2. Función tradicional con mysql.connector (para tickets.py)
def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            host=host,
            user=usuario,
            password=password,
            database=database
        )
        return conexion
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None