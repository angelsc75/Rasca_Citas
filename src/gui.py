import streamlit as st
from pymongo import MongoClient, errors
from dotenv import load_dotenv
import os
import time
from logging_config import setup_logger
from scrap_basic import scrap_basic
from scrap_confucius import scrap_confucious

# Configurar la página de Streamlit
st.set_page_config(
    page_title="El busca citas (~ frases)",
    page_icon="https://img.icons8.com/color/96/guru.png",
    layout="wide",
)

# Configurar el logger
logger = setup_logger()

# Cargar variables de entorno
load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')
DATABASE_NAME = os.getenv('DATABASE_NAME')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')

def perform_scraping(client):
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

# Inicializar el estado de sesión
if 'last_scraping_time' not in st.session_state:
    st.session_state.last_scraping_time = 0

# Ejecutar el scraping si han pasado 5 minutos
current_time = time.time()
time_interval = 300  # 5 minutos en segundos

if current_time - st.session_state.last_scraping_time > time_interval:
    perform_scraping(client)
    st.session_state.last_scraping_time = current_time

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

# Actualizar la interfaz principal en función del tiempo del último scraping
if 'last_scraping_time' in st.session_state:
    last_scraping_time = time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(st.session_state.last_scraping_time))
    st.write(f"Última ejecución del scraping: {last_scraping_time}")
else:
    st.write("Scraping no ejecutado.")



