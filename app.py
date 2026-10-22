from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

# Importamos los routers
from routes.tickets import router as tickets_router
from routes.usuarios import router as usuarios_router
from routes.auth import router as auth_router
from routes.ia import router as ia_router
from routes.activos import router as activos_router  # <-- Línea agregada para Activos

app = FastAPI(title="Pangea Help Desk IA", version="1.0")

# Carpeta para archivos estáticos (imágenes como el logo.png, estilos, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Incluimos los routers
app.include_router(tickets_router)
app.include_router(usuarios_router)
app.include_router(auth_router)
app.include_router(ia_router)
app.include_router(activos_router)  # <-- Línea agregada para Activos

# Ruta principal (Login)
@app.get("/", response_class=HTMLResponse)
def leer_index():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read(), status_code=200)

# Ruta para el Panel de Administración
@app.get("/dashboard", response_class=HTMLResponse)
def leer_dashboard():
    with open("templates/dashboard.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read(), status_code=200)

# Ruta para el Portal del Empleado
@app.get("/user_panel", response_class=HTMLResponse)
def leer_user_panel():
    with open("templates/user_dashboard.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read(), status_code=200)