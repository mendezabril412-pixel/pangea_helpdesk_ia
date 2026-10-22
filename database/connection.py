import mysql.connector
from sqlalchemy import create_engine, text

# Configuración de credenciales
usuario = "root"
password = "abril317"
host = "localhost"
database = "pangea_helpdesk_ia"

# 1. Engine de SQLAlchemy (para los módulos que lo requieran como usuarios.py)
conexion_url = f"mysql+pymysql://{usuario}:{password}@{host}/{database}"
engine = create_engine(conexion_url)

# 2. Función tradicional con mysql.connector (para tickets.py y los cursors)
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
    