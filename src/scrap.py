import requests
from bs4 import BeautifulSoup
import pandas as pd
import pymysql
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os



#load_dotenv()
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
    text = quote.find('span', class_='text').get_text()
    author = quote.find('small', class_='author').get_text()
    about = "https://quotes.toscrape.com" + quote.find('a')['href']
    keywords = [tag.get_text() for tag in quote.find_all('a', class_='tag')]
    data.append([text, author, about, keywords])

# Crear DataFrame
df = pd.DataFrame(data, columns=['quote', 'author', 'about', 'keywords'])

# Convertir la lista de keywords a una cadena separada por comas
#df['keywords'] = df['keywords'].apply(lambda x: ','.join(x))
print(df.head(10))




