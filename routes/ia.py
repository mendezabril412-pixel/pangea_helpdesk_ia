from fastapi import APIRouter
import ollama

router = APIRouter(prefix="/ia", tags=["Módulo de Inteligencia Artificial"])

@router.post("/consultar")
def consultar_ia(pregunta: str):
    try:
        response = ollama.chat(model='llama3.2', messages=[
            {
                'role': 'user',
                'content': pregunta,
            },
        ])
        return {
            "estado": "exito",
            "respuesta": response['message']['content']
        }
    except Exception as e:
        return {
            "estado": "error",
            "mensaje": str(e)
        }
    