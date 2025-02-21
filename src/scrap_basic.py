import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from pymongo.errors import OperationFailure
from dotenv import load_dotenv
import os
from logging_config import setup_logger

# Configurar el logger
logger = setup_logger()

def scrap_basic():
    # Cargar las variables de entorno desde el archivo .env
    load_dotenv()
    MONGO_URI = os.getenv('MONGO_URI')
    DATABASE_NAME = os.getenv('DATABASE_NAME')
    COLLECTION_NAME = os.getenv('COLLECTION_NAME')

    if not MONGO_URI or not DATABASE_NAME or not COLLECTION_NAME:
        logger.error("MONGO_URI, DATABASE_NAME o COLLECTION_NAME no están definidos en el archivo .env")
        raise ValueError("Asegúrate de que MONGO_URI, DATABASE_NAME y COLLECTION_NAME estén definidos en tu archivo .env")

    # Conectar a MongoDB
    try:
        client = MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]
    except Exception as e:
        logger.error(f"Error al conectar a MongoDB: {e}")
        raise

    # URL del sitio web
    base_url = "https://quotes.toscrape.com"

    # Iterar sobre las páginas
    for page_num in range(1, 11):  # Del 1 al 10 inclusive
        url = f"{base_url}/page/{page_num}"
        logger.info(f"Scraping {url}")

        # Realizar la petición
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Error al acceder a la URL: {url} - {e}")
            continue

        # Parsear la información
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontrar las citas
        quotes = soup.find_all('div', class_='quote')

        # Lista temporal para guardar las citas
        data = []

        # Iterar sobre las citas y extraer datos
        for quote in quotes:
            try:
                cita = quote.find('span', class_='text').get_text()
                author = quote.find('small', class_='author').get_text()

                # Procesar el nombre del autor
                author_parts = author.split()
                if len(author_parts) > 1:
                    author_slug = '-'.join(author_parts)
                else:
                    author_slug = author_parts[0]

                # Construir el enlace 'about' con el formato correcto
                about = f"http://quotes.toscrape.com/author/{author_slug}/"

                # Obtener las etiquetas
                keywords = [tag.get_text() for tag in quote.find_all('a', class_='tag')]

                # Verificar si la cita ya existe en la base de datos
                if not collection.find_one({'quote': cita, 'author': author}):
                    data.append({
                        'quote': cita,
                        'author': author,
                        'about': about,
                        'keywords': keywords
                    })
            except Exception as e:
                logger.error(f"Error al procesar una cita: {e}")
                continue

        if data:  # Solo intentar insertar si hay datos nuevos
            try:
                # Insertar los datos en la colección
                result = collection.insert_many(data)
                logger.info(f"Datos insertados exitosamente en la base de datos MongoDB. Número de documentos insertados: {len(result.inserted_ids)}")
            except OperationFailure as e:
                logger.error(f"Error de operación en MongoDB: {e.details}")
            except Exception as e:
                logger.error(f"Error al conectar o insertar en MongoDB: {e}")
        else:
            logger.info("No hay datos nuevos para insertar.")

# Ejecutar la función de scraping
if __name__ == "__main__":
    try:
        scrap_basic()
    except Exception as e:
        logger.error(f"Error al ejecutar el scraping: {e}")


