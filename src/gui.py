import streamlit as st
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')
DATABASE_NAME = os.getenv('DATABASE_NAME')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')

# Conectar a MongoDB
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Configurar la página de Streamlit
st.title("El rasca citas")
st.sidebar.header("Filtrado")

# Obtener todas las etiquetas y autores de la colección
tags = collection.distinct("keywords")
authors = collection.distinct("author")

# Crear selectores en la barra lateral
selected_tag = st.sidebar.selectbox("Select a tag", ["All"] + tags)
selected_author = st.sidebar.selectbox("Select an author", ["All"] + authors)

# Filtrar las citas según la etiqueta y el autor seleccionados
query = {}
if selected_tag != "All":
    query["keywords"] = selected_tag
if selected_author != "All":
    query["author"] = selected_author

quotes = collection.find(query)

# Mostrar las citas filtradas
if collection.count_documents(query) == 0:
    st.write("No quotes found.")
else:
    for quote in quotes:
        st.write(f"**{quote['quote']}**")
        st.write(f"— {quote['author']}")
        st.write(f"Tags: {', '.join(quote['keywords'])}")
        st.write(f"[About the author]({quote['about']})")
        st.write("---")

