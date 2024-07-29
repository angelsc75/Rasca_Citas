# Usa una imagen base de Python
FROM python:3.12

# Configura el directorio de trabajo
WORKDIR /app

# Copia el archivo de requerimientos al contenedor
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código fuente y los tests al contenedor
COPY src/ ./src



# Define el comando por defecto

COPY .env .env

CMD ["streamlit", "run", "src/main.py"]