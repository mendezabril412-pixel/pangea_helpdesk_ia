from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database.connection import obtener_conexion

router = APIRouter(prefix="/auth", tags=["Autenticación"])

class LoginSchema(BaseModel):
    correo: str
    password: str

@router.post("/login")
def login(data: LoginSchema):
    conexion = obtener_conexion()
    if not conexion:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
    
    try:
        cursor = conexion.cursor(dictionary=True)
        # Probamos primero con las columnas estándar
        cursor.execute("SELECT * FROM Usuarios WHERE correo = %s AND password = %s", (data.correo, data.password))
        usuario = cursor.fetchone()
        
        # Si no lo encuentra, probamos buscando por si las columnas se llaman diferente (ej. email / contrasena)
        if not usuario:
            cursor.execute("SELECT * FROM Usuarios WHERE email = %s AND password = %s", (data.correo, data.password))
            usuario = cursor.fetchone()
            
        cursor.close()
        conexion.close()
        
        if not usuario:
            raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")
        
        # Obtenemos el rol de forma segura
        rol = str(usuario.get("rol") or usuario.get("role") or "").lower()
        
        if "admin" in rol:
            redirect_url = "/dashboard"
        else:
            redirect_url = "/user_panel"
            
        return {
            "mensaje": "Login exitoso",
            "redirect": redirect_url,
            "rol": usuario.get("rol") or usuario.get("role") or "usuario",
            "id_usuario": usuario.get("id_usuario") or usuario.get("id") or 2
        }
        
    except Exception as e:
        if conexion:
            conexion.close()
        raise HTTPException(status_code=500, detail=f"Error en base de datos: {str(e)}")