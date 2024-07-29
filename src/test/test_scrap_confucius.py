# src/test/test_scrap_confucius.py
import sys
import os
import pytest
from unittest.mock import patch, MagicMock
# Añadir la carpeta src al PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
# Asegúrate de que la ruta es correcta
from scrap_confucius import scrap_confucius

@patch('scrap_confucius.requests.get')
@patch('scrap_confucius.MongoClient')
def test_scrap_confucius(mock_MongoClient, mock_requests_get):
    # Configurar el mock de requests
    mock_response = MagicMock()
    mock_response.text = '''
    <html>
        <body>
            <div class="quoteDetails">
                <div class="quoteText">"The greatest glory of living lies not in never falling, but in rising every time we fall.”</div>
                <div class="greyText smallText left">
                    <a class="authorTitle" href="#">wisdom</a>
                    <a class="authorTitle" href="#">life</a>
                </div>
            </div>
        </body>
    </html>
    '''
    mock_response.status_code = 200
    mock_requests_get.return_value = mock_response

    # Configurar el mock de MongoDB
    mock_collection = MagicMock()
    mock_collection.find_one.return_value = None  # Simula que la cita no existe en la DB
    mock_client = MagicMock()
    mock_client.__getitem__.return_value.__getitem__.return_value = mock_collection
    mock_MongoClient.return_value = mock_client

    # Llamar a la función de scraping
    scrap_confucius()

    # Verificar que se haya hecho una llamada a requests.get con la URL correcta
    mock_requests_get.assert_called_once_with(
        'https://www.goodreads.com/author/quotes/15321.Confucius',
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    )

    # Verificar que se intentó insertar el documento en la base de datos
    assert mock_collection.insert_many.called

    # Verificar los datos que se están insertando
    args, kwargs = mock_collection.insert_many.call_args
    documents = args[0]
    assert len(documents) == 1  # Asegúrate de que solo haya un documento insertado
    assert documents[0]['quote'] == '"The greatest glory of living lies not in never falling, but in rising every time we fall.”'
    assert documents[0]['author'] == 'Confucius'
    assert documents[0]['about'] == 'https://en.wikipedia.org/wiki/Confucius'
    assert 'wisdom' in documents[0]['keywords']
    assert 'life' in documents[0]['keywords']

