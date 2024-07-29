import sys
import os
from unittest.mock import patch, MagicMock
import pytest
import requests
from pymongo import MongoClient
from pymongo.errors import OperationFailure

# Añadir la carpeta src al PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from scrap_basic import scrap_basic

@patch('scrap_basic.requests.get')
@patch('scrap_basic.MongoClient')
def test_scrap_basic_success(mock_MongoClient, mock_requests_get):
    # Configurar el mock de requests
    mock_response = MagicMock()
    mock_response.text = '<html><body><div class="quote"><span class="text">Test quote</span><small class="author">Test Author</small><a class="tag">test</a></div></body></html>'
    mock_response.status_code = 200
    mock_requests_get.return_value = mock_response

    # Configurar el mock de MongoDB
    mock_collection = MagicMock()
    mock_collection.find_one.return_value = None  # Simula que la cita no existe en la DB    
    mock_client = MagicMock()
    mock_client.__getitem__.return_value.__getitem__.return_value = mock_collection
    mock_MongoClient.return_value = mock_client

    # Llamar a la función de scraping
    scrap_basic()

    # Verificar que se hayan hecho 10 llamadas
    assert mock_requests_get.call_count == 10, f"Expected 10 calls but got {mock_requests_get.call_count}"

    # Verificar que se hayan hecho llamadas a las URLs esperadas
    expected_urls = [f'https://quotes.toscrape.com/page/{i}' for i in range(1, 11)]
    actual_urls = [call[0][0] for call in mock_requests_get.call_args_list]
    
    for url in expected_urls:
        assert url in actual_urls, f"Expected URL {url} not found in {actual_urls}"



