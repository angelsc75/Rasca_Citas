import streamlit as st
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import time
from scrap_basic import scrap_basic
from scrap_confucius import scrap_confucious

# Cargar variables de entorno
load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')
DATABASE_NAME = os.getenv('DATABASE_NAME')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')

# Conectar a MongoDB
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Configurar la página de Streamlit
st.set_page_config(
    page_title="El busca citas (~ frases)",
    page_icon="https://img.icons8.com/color/96/guru.png",  # URL de la imagen directamente
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

# Barra lateral 


# Agregar el botón para iniciar/detener el scraping en la barra lateral
if 'scraping_active' not in st.session_state:
    st.session_state.scraping_active = False

def toggle_scraping():
    st.session_state.scraping_active = not st.session_state.scraping_active

st.sidebar.button('Iniciar/Detener Scraping', on_click=toggle_scraping)

# Mostrar el estado actual en la barra lateral
if st.session_state.scraping_active:
    st.sidebar.write("El scraping está ACTIVADO. El script se ejecutará cada 3 minutos.")
else:
    st.sidebar.write("El scraping está DESACTIVADO. El script no se está ejecutando.")

st.sidebar.header("Filtrado")
# Obtener todas las etiquetas y autores de la colección
tags = collection.distinct("keywords")
authors = collection.distinct("author")

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

# Ejecutar el script cada 3 minutos si el scraping está activado
if st.session_state.scraping_active:
    while True:
        scrap_confucious()
        scrap_basic()
        st.write("Scraping ejecutado. Esperando 3 minutos antes de la próxima ejecución...")
        time.sleep(180.0)  # Esperar 180 segundos (3 minutos)




