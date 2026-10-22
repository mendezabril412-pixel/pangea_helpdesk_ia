from fastapi import APIRouter, HTTPException, Form
from pydantic import BaseModel
from typing import Optional
from database.connection import obtener_conexion

router = APIRouter(prefix="/tickets", tags=["Tickets"])

class TicketSchema(BaseModel):
    titulo: str
    descripcion: str
    categoria: Optional[str] = "Soporte General"
    prioridad: Optional[str] = 'Media'
    estado: Optional[str] = 'Nuevo'
    id_usuario: int = 1

@router.post("/")
def crear_ticket(ticket: TicketSchema):
    conexion = obtener_conexion()
    if not conexion:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
    try:
        cursor = conexion.cursor()
        query = """
            INSERT INTO Tickets 
            (titulo, descripcion, categoria, prioridad, estado, id_usuario) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        valores = (
            ticket.titulo, 
            ticket.descripcion, 
            ticket.categoria, 
            ticket.prioridad, 
            ticket.estado, 
            ticket.id_usuario
        )
        cursor.execute(query, valores)
        conexion.commit()
        nuevo_id = cursor.lastrowid
        
        cursor.close()
        conexion.close()
        
        return {"mensaje": "Ticket creado exitosamente", "id_ticket": nuevo_id}
    except Exception as e:
        print(f"Error al insertar ticket: {e}")
        raise HTTPException(status_code=500, detail="Error interno al crear el ticket")

@router.get("/")
def listar_tickets():
    conexion = obtener_conexion()
    if not conexion:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT id_ticket, titulo, descripcion, categoria, prioridad, estado, fecha_creacion FROM Tickets")
        resultado = cursor.fetchall()
        cursor.close()
        conexion.close()
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id_ticket}")
def obtener_detalle_ticket(id_ticket: int):
    conexion = obtener_conexion()
    if not conexion:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
    try:
        cursor = conexion.cursor(dictionary=True)
        
        # 1. Traer la información principal del ticket
        cursor.execute(
            "SELECT id_ticket, titulo, descripcion, categoria, prioridad, estado, fecha_creacion FROM Tickets WHERE id_ticket = %s", 
            (id_ticket,)
        )
        ticket = cursor.fetchone()
        
        if not ticket:
            cursor.close()
            conexion.close()
            raise HTTPException(status_code=404, detail="Ticket no encontrado")
            
        # 2. Traer todo el seguimiento/comentarios de ese ticket
        cursor.execute(
            "SELECT comentario, creado_por, fecha_registro FROM Ticket_Comentarios WHERE id_ticket = %s ORDER BY fecha_registro ASC", 
            (id_ticket,)
        )
        comentarios = cursor.fetchall()
        
        # 3. Empaquetar el ticket junto con su retroalimentación
        ticket["historial_comentarios"] = comentarios
        
        cursor.close()
        conexion.close()
        
        return ticket
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/actualizar/{id_ticket}")
def actualizar_ticket(
    id_ticket: int,
    id_area_soporte: int = Form(...),
    estado: str = Form(...),
    comentario: str = Form(...)
):
    conexion = obtener_conexion()
    if not conexion:
        raise HTTPException(status_code=500, detail="Error de conexión a la BD")
    try:
        cursor = conexion.cursor()
        # 1. Actualizamos el área de soporte y estado en MySQL
        cursor.execute(
            "UPDATE Tickets SET id_area_soporte = %s, estado = %s WHERE id_ticket = %s",
            (id_area_soporte, estado, id_ticket)
        )
        # 2. Guardamos la retroalimentación en la tabla de comentarios
        cursor.execute(
            "INSERT INTO Ticket_Comentarios (id_ticket, comentario, creado_por) VALUES (%s, %s, %s)",
            (id_ticket, comentario, "Administrador")
        )
        conexion.commit()
        cursor.close()
        conexion.close()
        return {"mensaje": "Ticket actualizado y retroalimentado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))