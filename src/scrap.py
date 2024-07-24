import requests
from bs4 import BeautifulSoup
import pandas as pd
from pymongo import MongoClient
from pymongo.errors import OperationFailure
from dotenv import load_dotenv
import os

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
base_url = "https://quotes.toscrape.com"

# Iterar sobre las páginas
for page_num in range(1, 11):  # Del 1 al 10 inclusive
    url = f"{base_url}/page/{page_num}/"
    print(f"Scraping {url}")

    # Realizar la petición
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error al acceder a la URL: {url}")
        continue

    # Parsear la información
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontrar las citas
    quotes = soup.find_all('div', class_='quote')

    # Lista temporal para guardar las citas
    data = []

    # Iterar sobre las citas y extraer datos
    for quote in quotes:
        cita = quote.find('span', class_='text').get_text()
        author = quote.find('small', class_='author').get_text()
        about = url + quote.find('a')['href']
        keywords = [tag.get_text() for tag in quote.find_all('a', class_='tag')]
        # Verificar si la cita ya existe en la base de datos
        if not collection.find_one({'quote': cita, 'author': author}):
            data.append({
                'quote': cita,
                'author': author,
                'about': about,
                'keywords': keywords
            })

    # Crear DataFrame
    df = pd.DataFrame(data)
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
