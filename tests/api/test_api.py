import unittest
from unittest.mock import patch, MagicMock
import numpy as np

from fastapi.testclient import TestClient
from challenge.api import app  # Asegúrate de que la ruta sea correcta

class TestAPIPredict(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
    
    @patch('challenge.api.model.preprocess')
    @patch('challenge.api.model._model.predict')
    def test_predict_success(self, mock_predict, mock_preprocess):
        # Configurar el mock
        mock_preprocess.return_value = MagicMock()
        mock_predict.return_value = np.array([0])
        
        # Datos de prueba
        data = {
            "flights": [
                {
                    "OPERA": "Aerolineas Argentinas", 
                    "TIPOVUELO": "N", 
                    "MES": 3
                }
            ]
        }
        
        response = self.client.post("/predict", json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"predict": [0]})
        
        # Verificar que se llamó al preprocesamiento y predict
        mock_preprocess.assert_called_once()
        mock_predict.assert_called_once()
    
    @patch('challenge.api.model.preprocess')
    @patch('challenge.api.model._model.predict')
    def test_predict_multiple_flights(self, mock_predict, mock_preprocess):
        # Configurar el mock
        mock_preprocess.return_value = MagicMock()
        mock_predict.return_value = np.array([0, 1])
        
        # Datos de prueba con múltiples vuelos
        data = {
            "flights": [
                {
                    "OPERA": "Aerolineas Argentinas", 
                    "TIPOVUELO": "N", 
                    "MES": 3
                },
                {
                    "OPERA": "Sky Airline", 
                    "TIPOVUELO": "I", 
                    "MES": 7
                }
            ]
        }
        
        response = self.client.post("/predict", json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"predict": [0, 1]})
        
        # Verificar que se llamó al preprocesamiento y predict
        mock_preprocess.assert_called_once()
        mock_predict.assert_called_once()
    
    @patch('challenge.api.model.preprocess')
    @patch('challenge.api.model._model.predict')
    def test_predict_empty_flights(self, mock_predict, mock_preprocess):
        # Configurar el mock
        mock_preprocess.return_value = MagicMock()
        mock_predict.return_value = np.array([])
        
        # Datos de prueba con lista de vuelos vacía
        data = {
            "flights": []
        }
        
        response = self.client.post("/predict", json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"predict": []})
        
        # Verificar que se llamó al preprocesamiento y predict
        mock_preprocess.assert_called_once()
        mock_predict.assert_called_once()
    
    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "OK", "detail": "your request was received"})
    
    def test_predict_missing_flights_key(self):
        # Payload sin la clave 'flights'
        data = {
            "flight": [  # Clave incorrecta
                {
                    "OPERA": "Aerolineas Argentinas", 
                    "TIPOVUELO": "N", 
                    "MES": 3
                }
            ]
        }
        
        response = self.client.post("/predict", json=data)
        self.assertEqual(response.status_code, 422)  # Error de validación de Pydantic
        self.assertIn("value_error.missing", response.text)
    
    @patch('challenge.api.model.preprocess')
    @patch('challenge.api.model._model.predict')
    def test_predict_invalid_mes(self, mock_predict, mock_preprocess):
        # Configurar el mock para manejar MES inválido
        mock_preprocess.side_effect = ValueError("MES inválido")
        
        data = {
            "flights": [
                {
                    "OPERA": "Aerolineas Argentinas",
                    "TIPOVUELO": "N",
                    "MES": 13  # Inválido
                }
            ]
        }
        
        response = self.client.post("/predict", json=data)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"detail": "MES inválido"})
    
    @patch('challenge.api.model.preprocess')
    @patch('challenge.api.model._model.predict')
    def test_predict_invalid_tipovuelo(self, mock_predict, mock_preprocess):
        # Configurar el mock para manejar TIPOVUELO inválido
        mock_preprocess.side_effect = ValueError("TIPOVUELO inválido")
        
        data = {
            "flights": [
                {
                    "OPERA": "Aerolineas Argentinas",
                    "TIPOVUELO": "O",  # Inválido
                    "MES": 3
                }
            ]
        }
        
        response = self.client.post("/predict", json=data)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"detail": "TIPOVUELO inválido"})
    
    @patch('challenge.api.model.preprocess')
    def test_predict_preprocess_exception(self, mock_preprocess):
        # Simular una excepción durante el preprocesamiento
        mock_preprocess.side_effect = Exception("Error durante el preprocesamiento")
        
        data = {
            "flights": [
                {
                    "OPERA": "Aerolineas Argentinas",
                    "TIPOVUELO": "N",
                    "MES": 3
                }
            ]
        }
        
        response = self.client.post("/predict", json=data)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"detail": "Error durante el preprocesamiento"})
    
    @patch('challenge.api.model.preprocess')
    @patch('challenge.api.model._model.predict')
    def test_predict_predict_exception(self, mock_predict, mock_preprocess):
        # Configurar el mock para lanzar una excepción durante la predicción
        mock_preprocess.return_value = MagicMock()
        mock_predict.side_effect = Exception("Error durante la predicción")
        
        data = {
            "flights": [
                {
                    "OPERA": "Aerolineas Argentinas",
                    "TIPOVUELO": "N",
                    "MES": 3
                }
            ]
        }
        
        response = self.client.post("/predict", json=data)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"detail": "Error durante la predicción"})
    
    @patch('challenge.api.model.preprocess')
    @patch('challenge.api.model._model.predict')
    def test_predict_unknown_opera(self, mock_predict, mock_preprocess):
        # Configurar el mock para manejar una OPERA desconocida
        mock_preprocess.return_value = MagicMock()
        mock_predict.return_value = np.array([0])
        
        data = {
            "flights": [
                {
                    "OPERA": "Unknown Airline",
                    "TIPOVUELO": "N",
                    "MES": 3
                }
            ]
        }
        
        response = self.client.post("/predict", json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"predict": [0]})
        
        mock_preprocess.assert_called_once()
        mock_predict.assert_called_once()

if __name__ == '__main__':
    unittest.main()
