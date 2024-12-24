import logging
from typing import List
import pandas as pd
import joblib

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from xgboost import XGBClassifier
from challenge.model import DelayModel  

# Configuración de Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Definición de modelos Pydantic para el request
class Flight(BaseModel):
    OPERA: str = Field(..., example="Aerolineas Argentinas")
    TIPOVUELO: str = Field(..., example="N")
    MES: int = Field(..., example=3)

class FlightRequest(BaseModel):
    flights: List[Flight] = Field(
        ...,
        example=[
            {
                "OPERA": "Aerolineas Argentinas", 
                "TIPOVUELO": "N", 
                "MES": 3
            }
        ]
    )


# Inicialización de la aplicación FastAPI
app = FastAPI(
    title="Modelo de Predicción de Retrasos de Vuelos",
    description="API para predecir retrasos de vuelos basado en características como OPERA, TIPOVUELO y MES.",
    version="1.0.0"
)

# ----------------------------------------------------------------
# Carga del modelo entrenado y los artefactos
# ----------------------------------------------------------------
model = DelayModel(
    model_path='challenge/delay_model.json',
    columns_path='challenge/fitted_columns.pkl',
    scaler_path='challenge/scaler.pkl'
)

# Cargar el modelo desde el archivo JSON
loaded_xgb = XGBClassifier()
loaded_xgb.load_model(model._model_json_path)
model._model = loaded_xgb
logger.info(f"✅ Modelo cargado desde {model._model_json_path}")

# Cargar las columnas y el scaler
model._fitted_columns = joblib.load(model._columns_path)
model._scaler = joblib.load(model._scaler_path)
logger.info(f"✅ Columnas cargadas desde {model._columns_path} y scaler desde {model._scaler_path}")

# ----------------------------------------------------------------
# Endpoint de Salud
# ----------------------------------------------------------------
@app.get("/health", status_code=200)
async def get_health() -> dict:
    """
    Endpoint para verificar el estado de la API.
    """
    return {"status": "OK", "detail": "your request was received"}

# ----------------------------------------------------------------
# Endpoint de Predicción
# ----------------------------------------------------------------
@app.post("/predict", status_code=200)
async def post_predict(request: FlightRequest) -> dict:
    """
    Endpoint para predecir retrasos de vuelos.
    
    **Ejemplo de Payload:**
    
    ```json
    {
      "flights": [
        {
          "OPERA": "Aerolineas Argentinas", 
          "TIPOVUELO": "N", 
          "MES": 3
        }
      ]
    }
    ```
    
    **Respuesta Exitosa:**
    
    ```json
    {
      "predict": [0]
    }
    ```
    """
    try:
        flights_list = [flight.dict() for flight in request.flights]
        df_inference = pd.DataFrame(flights_list)
        logger.info(f"🔄 Datos de inferencia recibidos: {df_inference}")

        # Preprocesamiento en modo inferencia
        df_processed = model.preprocess(
            df_inference,
            fit=False,
            is_training=False
        )
        logger.info(f"🔄 Datos preprocesados: {df_processed}")

        # Predicción
        preds = model._model.predict(df_processed)
        logger.info(f"🔄 Predicciones realizadas: {preds}")

        # Retornar respuesta
        return {"predict": preds.tolist()}

    except Exception as e:
        logger.error(f"❌ Error en /predict: {e}")
        raise HTTPException(status_code=500, detail=str(e))
