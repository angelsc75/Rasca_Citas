import streamlit as st
from pymongo import MongoClient, errors
from dotenv import load_dotenv
import os
import time
from logging_config import setup_logger
from scrap_basic import scrap_basic
from scrap_confucius import scrap_confucious

# Configurar el logger
logger = setup_logger()

# Cargar variables de entorno
load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')
DATABASE_NAME = os.getenv('DATABASE_NAME')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')

# Conectar a MongoDB
try:
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    logger.info("Conexión a MongoDB exitosa.")
except errors.ConnectionError as e:
    logger.error(f"Error al conectar a MongoDB: {e}")
    st.error("No se pudo conectar a la base de datos MongoDB. Revisa los detalles en el log.")
    st.stop()

# Configurar la página de Streamlit
st.set_page_config(
    page_title="El busca citas (~ frases)",
    page_icon="https://img.icons8.com/color/96/guru.png",
    layout="wide",
)

# Agregar un banner
st.markdown("""
    <style>
        .banner {
            text-align: center;
            padding: 2rem;
            background-color: #f2f2f2;
            border-bottom: 2px solid #ccc;
        }
        .banner img {
            max-width: 100%;
            height: auto;
        }
    </style>
    <div class="banner">
        <img src="https://img.icons8.com/color/96/guru.png" alt="Banner">
        <h1>El busca citas (~ frases)</h1>
    </div>
""", unsafe_allow_html=True)

# Inicializar las variables de estado de sesión
if 'scraping_active' not in st.session_state:
    st.session_state.scraping_active = False
if 'last_scraping_time' not in st.session_state:
    st.session_state.last_scraping_time = 0
if 'next_scraping_time' not in st.session_state:
    st.session_state.next_scraping_time = 0

def start_scraping():
    st.session_state.scraping_active = True
    st.session_state.next_scraping_time = time.time() + 180  # Tiempo para la próxima ejecución (3 minutos)
    logger.info("Scraping iniciado.")
    st.write("Scraping iniciado.")

def stop_scraping():
    st.session_state.scraping_active = False
    st.session_state.next_scraping_time = 0
    logger.info("Scraping detenido.")
    st.write("Scraping detenido.")

# Botones para iniciar y detener el scraping en la barra lateral
st.sidebar.button('Iniciar Scraping', on_click=start_scraping)
st.sidebar.button('Detener Scraping', on_click=stop_scraping)

# Mostrar el estado actual en la barra lateral
if st.session_state.scraping_active:
    st.sidebar.write("El scraping está ACTIVADO. El script se ejecutará cada 3 minutos.")
else:
    st.sidebar.write("El scraping está DESACTIVADO. El script no se está ejecutando.")

# Mostrar la última vez que se ejecutó el scraping
last_scraping_time = st.session_state.last_scraping_time
if last_scraping_time:
    last_scraping_time_formatted = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_scraping_time))
    st.sidebar.write(f"Última ejecución del scraping: {last_scraping_time_formatted}")

def perform_scraping():
    logger.info("Inicio del proceso de scraping.")
    st.write("Inicio del proceso de scraping.")  # Para verificar visualmente
    try:
        scrap_confucious()
        scrap_basic()
        logger.info("Scraping completado con éxito.")
        st.write("Scraping completado con éxito.")  # Para verificar visualmente
    except Exception as e:
        logger.error(f"Error durante el scraping: {e}")
        st.error("Hubo un error durante el scraping. Revisa los detalles en el log.")

# Ejecutar el scraping si está activo y el tiempo actual es mayor que el tiempo de la próxima ejecución
if st.session_state.scraping_active:
    current_time = time.time()
    st.write(f"Tiempo actual: {current_time}")
    st.write(f"Próxima ejecución programada: {st.session_state.next_scraping_time}")
    if st.session_state.next_scraping_time and current_time >= st.session_state.next_scraping_time:
        perform_scraping()
        st.session_state.last_scraping_time = current_time
        st.session_state.next_scraping_time = current_time + 180  # Establecer el tiempo para la próxima ejecución

st.sidebar.header("Filtrado")
# Obtener todas las etiquetas y autores de la colección
try:
    tags = collection.distinct("keywords")
    authors = collection.distinct("author")
except Exception as e:
    logger.error(f"Error al obtener etiquetas o autores de la colección: {e}")
    st.error("No se pudieron obtener las etiquetas o autores. Revisa los detalles en el log.")
    tags = []
    authors = []

# Crear selectores en la barra lateral
selected_tag = st.sidebar.selectbox("Selección por una etiqueta", ["All"] + tags)
selected_tags = st.sidebar.multiselect("Selecciona por una o más etiquetas", tags)
selected_author = st.sidebar.selectbox("Selección por autor", ["All"] + authors)

# Filtrar las citas según la etiqueta y el autor seleccionados
query = {}
if selected_tag != "All":
    query["keywords"] = selected_tag
if selected_tags:
    query["keywords"] = {"$all": selected_tags}

if selected_author != "All":
    query["author"] = selected_author

# Mostrar las citas filtradas
try:
    if collection.count_documents(query) == 0:
        st.write("No quotes found.")
    else:
        st.write(f' **Citas encontradas: {collection.count_documents(query)}**')
        st.write("---")
        quotes = collection.find(query)
        for quote in quotes:
            st.write(f"**{quote['quote']}**")
            st.write(f"— {quote['author']}")
            st.write(f"Tags: {', '.join(quote['keywords'])}")
            st.write(f"[About the author]({quote['about']})")
            st.write("---")
except Exception as e:
    logger.error(f"Error al mostrar citas: {e}")
    st.error("Hubo un error al mostrar las citas. Revisa los detalles en el log.")

# Mostrar el estado de scraping en la interfaz principal
if st.session_state.scraping_active:
    st.write("Scraping en progreso...")

# Actualizar la interfaz principal en función del tiempo del último scraping
if st.session_state.last_scraping_time:
    last_scraping_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(st.session_state.last_scraping_time))
    st.write(f"Última ejecución del scraping: {last_scraping_time}")





