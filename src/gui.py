import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Configura tu conexión a la base de datos
DATABASE_URL = 'mysql+pymysql://root:admin@localhost/scraping_quotes'
engine = create_engine(DATABASE_URL)

# Configuración de la página
st.set_page_config(page_title="Visualización de Datos", layout="wide")

# Título de la aplicación
st.title("Visualización de Datos con Streamlit")

# Función para cargar datos
@st.cache_data
def load_data():
    query = "SELECT * FROM quotes;"  # Ajusta la consulta según tu tabla
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df

# Cargar datos
data = load_data()

# Mostrar los datos en la aplicación
st.write("### Datos de la Tabla Quotes")
st.dataframe(data)

# Mostrar gráficos básicos
st.write("### Gráficos Básicos")
st.bar_chart(data['id'])