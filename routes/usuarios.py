from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from database.connection import engine

router = APIRouter()

class UsuarioCreate(BaseModel):
    num_empleado: str
    nombre: str
    apellido_paterno: str
    apellido_materno: str | None = None
    email: str
    telefono: str | None = None
    id_area: int

@router.get("/usuarios")
def listar_usuarios():
    with engine.connect() as conn:
        resultado = conn.execute(
            text("SELECT num_empleado, nombre, apellido_paterno, apellido_materno, email, telefono, id_area FROM Usuarios")
        )
        usuarios = []
        for fila in resultado:
            usuarios.append({
                "num_empleado": fila.num_empleado,
                "nombre": fila.nombre,
                "apellido_paterno": fila.apellido_paterno,
                "apellido_materno": fila.apellido_materno,
                "email": fila.email,
                "telefono": fila.telefono,
                "id_area": fila.id_area
            })
        return usuarios

@router.post("/usuarios")
def crear_usuario(usuario: UsuarioCreate):
    try:
        with engine.connect() as conn:
            query = text("""
                INSERT INTO Usuarios (num_empleado, nombre, apellido_paterno, apellido_materno, email, telefono, id_area)
                VALUES (:num_empleado, :nombre, :apellido_paterno, :apellido_materno, :email, :telefono, :id_area)
            """)
            conn.execute(query, {
                "num_empleado": usuario.num_empleado,
                "nombre": usuario.nombre,
                "apellido_paterno": usuario.apellido_paterno,
                "apellido_materno": usuario.apellido_materno,
                "email": usuario.email,
                "telefono": usuario.telefono,
                "id_area": usuario.id_area
            })
            conn.commit()
        return {"mensaje": "Usuario registrado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    