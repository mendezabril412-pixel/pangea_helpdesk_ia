import streamlit as st
import requests

# Configuración de la página
st.set_page_config(
    page_title="Pangea Help Desk - Pangi IA",
    page_icon="🐾",
    layout="centered"
)

# Estilos CSS personalizados para un diseño moderno y limpio
st.markdown("""
    <style>
    .main {
        background-color: #f4f6f9;
    }
    .pangi-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.08);
        border-left: 6px solid #ff7b00;
        margin-bottom: 20px;
    }
    .chat-title {
        color: #2c3e50;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Encabezado con la identidad de Pangi
col_img, col_txt = st.columns([1, 4])

with col_img:
    # Si tienes tu foto de Pangi guardada en tu proyecto, puedes cambiar '' 
    # por la ruta de tu imagen real. Por ahora te pongo un ejemplo visual:
    st.image("watermarked_img_11887736236319719627.jpg", width=100, caption="¡Hola, soy Pangi!")

with col_txt:
    st.title("Pangea Help Desk con Pangi 🐾")
    st.markdown("¡Hola! Soy Pangi, tu asistente de soporte técnico de confianza. Cuéntame qué problema tienes y te ayudaré a solucionarlo o a levantar un ticket.")

st.divider()

# Sección de consulta
st.markdown("### 💬 Escríbele a Pangi")
pregunta_usuario = st.text_area("¿Qué inconveniente técnico tienes hoy?", placeholder="Ej. No tengo internet en mi área de trabajo...")

if st.button("Preguntar a Pangi 🚀", type="primary"):
    if pregunta_usuario.strip() != "":
        with st.spinner("Pangi está analizando tu caso... 🤖"):
            try:
                # Petición a tu API de FastAPI
                response = requests.post(
                    "http://127.0.0.1:8000/ia/chat",
                    json={"pregunta": pregunta_usuario}
                )
                
                if response.status_code == 200:
                    datos = response.json()
                    st.success("¡Pangi ha encontrado una respuesta!")
                    
                    # Mostrar la respuesta con el estilo de Pangi
                    st.markdown(f"""
                        <div class="pangi-card">
                            <h4 class="chat-title">💡 Respuesta de Pangi:</h4>
                            <p>{datos['respuesta_sugerida']}</p>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error(f"Error en el servidor: {response.json().get('detail', 'Desconocido')}")
            except requests.exceptions.ConnectionError:
                st.error("No se pudo conectar con FastAPI. Asegúrate de que Uvicorn esté corriendo en la terminal.")
    else:
        st.warning("Por favor escribe una descripción del problema antes de enviársela a Pangi.")

        