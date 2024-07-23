import requests
from bs4 import BeautifulSoup
import pandas as pd
import pymysql
from sqlalchemy import create_engine, text

# URL del sitio web
url = "https://quotes.toscrape.com/"

# Realizar la petición
response = requests.get(url)

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
    about = "https://quotes.toscrape.com" + quote.find('a')['href']
    keywords = [tag.get_text() for tag in quote.find_all('a', class_='tag')]
    data.append([cita, author, about, keywords])

# Crear DataFrame
df = pd.DataFrame(data, columns=['quote', 'author', 'about', 'keywords'])

# Convertir la lista de keywords a una cadena separada por comas
df['keywords'] = df['keywords'].apply(lambda x: ','.join(x))

# Configurar la conexión a MySQL
user = 'root'
password = 'admin'
host = 'localhost'
database = 'scraping_quotes'

# Crear la conexión a la base de datos
engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}/{database}')

# Crear la tabla si no existe
create_table_query = """
CREATE TABLE IF NOT EXISTS quotes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    quote TEXT,
    author VARCHAR(255),
    about VARCHAR(255),
    keywords TEXT
);
"""


# Ejecutar la consulta
with engine.connect() as conn:
    conn.execute(text(create_table_query))
# Insertar los datos en la tabla
df.to_sql('quotes', con=engine, if_exists='append', index=False)

print("Datos insertados exitosamente en la base de datos.")




