from pymongo import MongoClient

# Conectar a MongoDB con autenticación
client = MongoClient('mongodb://localhost:27017/')

# Seleccionar base de datos y colección
db = client['scraping_quotes']
collection = db['coll1']

# Datos a insertar
data = [
    {"name": "Alice", "email": "alice@example.com"},
    {"name": "Bob", "email": "bob@example.com"}
]

# Insertar documentos
try:
    result = collection.insert_many(data)
    print("Documentos insertados con éxito.")
except Exception as e:
    print(f"Error al insertar documentos: {e}")
