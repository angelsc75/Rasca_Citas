import requests
from bs4 import BeautifulSoup
import pandas as pd
from pymongo import MongoClient
from pymongo.errors import OperationFailure
from dotenv import load_dotenv
import os

def scrap_confucious():
    # Cargar las variables de entorno desde el archivo .env
    load_dotenv()
    MONGO_URI = os.getenv('MONGO_URI')
    DATABASE_NAME = os.getenv('DATABASE_NAME')
    COLLECTION_NAME = os.getenv('COLLECTION_NAME')

    if not MONGO_URI or not DATABASE_NAME or not COLLECTION_NAME:
        raise ValueError("Asegúrate de que MONGO_URI, DATABASE_NAME y COLLECTION_NAME estén definidos en tu archivo .env")

    # Conectar a MongoDB
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]

    # URL del sitio web
    base_url = "https://www.goodreads.com/author/quotes/15321.Confucius"

    # Cabeceras para imitar un navegador
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Realizar la petición
    response = requests.get(base_url, headers=headers)
    if response.status_code != 200:
        print(f"Error al acceder a la URL: {base_url}")
    else:
        # Parsear la información
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontrar las citas
        quotes = soup.find_all('div', class_='quoteDetails')

        # Lista temporal para guardar las citas
        data = []

        # Iterar sobre las citas y extraer datos
        for quote in quotes:
            # Extraer el texto de la cita
            quote_text = quote.find('div', class_='quoteText').get_text(strip=True, separator=" ").split('”')[0] + '”'
            author = "Confucius"
            about = "https://en.wikipedia.org/wiki/Confucius"

            # Extraer etiquetas
            tags_div = quote.find_next('div', class_='greyText smallText left')
            if tags_div:
                keywords = [a_tag.get_text(strip=True) for a_tag in tags_div.find_all('a')]
            else:
                keywords = []  # No hay etiquetas disponibles si tags_div es None

            # Verificar si la cita ya existe en la base de datos
            if not collection.find_one({'quote': quote_text, 'author': author}):
                data.append({
                    'quote': quote_text,
                    'author': author,
                    'about': about,
                    'keywords': keywords
                })

        
        if data:  # Solo intentar insertar si hay datos nuevos
            try:
                # Insertar los datos en la colección
                result = collection.insert_many(data)
                print(f"Datos insertados exitosamente en la base de datos MongoDB. Número de documentos insertados: {len(result.inserted_ids)}")
            except OperationFailure as e:
                print(f"Error de operación en MongoDB: {e.details}")
            except Exception as e:
                print(f"Error al conectar o insertar en MongoDB: {e}")
        else:
            print("No hay datos nuevos para insertar.")

