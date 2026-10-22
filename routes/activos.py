from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database.connection import obtener_conexion

router = APIRouter(prefix="/activos", tags=["Activos TI"])

class ActivoSchema(BaseModel):
    tipo_equipo: str
    nombre_equipo: str
    numero_serie: str
    marca: str
    modelo: str
    id_usuario: int

@router.post("/")
def registrar_activo(activo: ActivoSchema):
    conexion = obtener_conexion()
    if not conexion:
        raise HTTPException(status_code=500, detail="Error de conexión a la BD")
    try:
        cursor = conexion.cursor()
        query = """
            INSERT INTO Activos_TI 
            (tipo_equipo, nombre_equipo, numero_serie, marca, modelo, id_usuario) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        valores = (activo.tipo_equipo, activo.nombre_equipo, activo.numero_serie, activo.marca, activo.modelo, activo.id_usuario)
        cursor.execute(query, valores)
        conexion.commit()
        nuevo_id = cursor.lastrowid
        cursor.close()
        conexion.close()
        return {"mensaje": "Activo registrado exitosamente", "id_activo": nuevo_id}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error al registrar el activo")

@router.get("/")
def listar_activos():
    conexion = obtener_conexion()
    if not conexion:
        raise HTTPException(status_code=500, detail="Error de conexión a la BD")
    try:
        cursor = conexion.cursor(dictionary=True)
        # Hacemos un JOIN con Usuarios para mostrar a quién pertenece el equipo
        cursor.execute("""
            SELECT a.id_activo, a.tipo_equipo, a.nombre_equipo, a.numero_serie, 
                   a.marca, a.modelo, u.nombre AS nombre_usuario 
            FROM Activos_TI a 
            LEFT JOIN Usuarios u ON a.id_usuario = u.id_usuario
            ORDER BY a.id_activo DESC
        """)
        activos = cursor.fetchall()
        cursor.close()
        conexion.close()
        return activos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))