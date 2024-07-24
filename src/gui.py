import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Configura tu conexión a la base de datos
#DATABASE_URL = 'mysql+pymysql://root:admin@localhost/scraping_quotes'
load_dotenv()  # Carga las variables del archivo .env

DATABASE_URL = os.getenv('DATABASE_URL')
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


# Mostrar opciones
option = st.selectbox('Selecciona una opción:', ['Opción 1', 'Opción 2'])

# mostrar gráficos avanzados

fig, ax = plt.subplots()
sns.histplot(data['some_column'], ax=ax)
st.pyplot(fig)

# interactividad

if st.button('Mostrar Mensaje'):
    st.write('¡Botón presionado!')
# layouts y diseños

col1, col2 = st.columns(2)
with col1:
    st.write("Columna 1")
with col2:
    st.write("Columna 2")
