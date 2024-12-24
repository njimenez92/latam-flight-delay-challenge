import pandas as pd
import logging
from typing import Tuple, Union, List, Optional
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from xgboost import XGBClassifier
import joblib

# Para early stopping
from sklearn.model_selection import StratifiedKFold

from utils.utils import (
    get_period_day,
    is_high_season,
    get_min_diff,
    delay
)

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Define important features as a constant
IMPORTANT_FEATURES = [
    'OPERA_Latin American Wings',
    'MES_7',
    'MES_10',
    'OPERA_Grupo LATAM',
    'MES_12',
    'TIPOVUELO_I',
    'MES_4',
    'MES_11',
    'OPERA_Sky Airline',
    'OPERA_Copa Air'
]

class DelayModel:
    def __init__(
        self, 
        important_features: Optional[List[str]] = None,
        model_path: str = 'challenge/delay_model.json',   # Se guarda en JSON (XGBoost)
        columns_path: str = 'challenge/fitted_columns.pkl',
        scaler_path: str = 'challenge/scaler.pkl'
    ):
        """
        Constructor por defecto. 
        """
        self._model = XGBClassifier(
            random_state=42,
            eval_metric='logloss'
        )
        self._scaler = StandardScaler()
        self._important_features = important_features or IMPORTANT_FEATURES
        self._fitted_columns = None
        self._model_json_path = model_path
        self._columns_path = columns_path
        self._scaler_path = scaler_path

    # ----------------------------------------------------------------
    # Genera columnas de fecha (SOLO para entrenamiento)
    # ----------------------------------------------------------------
    def generate_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Crea columnas period_day, high_season, min_diff 
        a partir de 'Fecha-I'. Se asume que 'Fecha-I' existe.
        """
        logger.info("🔄 Generating date-based features...")
        data['period_day'] = data['Fecha-I'].apply(get_period_day)
        data['high_season'] = data['Fecha-I'].apply(is_high_season)
        data['min_diff'] = data.apply(get_min_diff, axis=1)
        logger.info("✅ Date-based features generated successfully.")
        return data

    def add_delay_column(self, data: pd.DataFrame, threshold: int = 15) -> pd.DataFrame:
        """
        Crea la columna 'delay' a partir de 'min_diff' (0/1).
        Esto se usa en entrenamiento para definir el target.
        """
        data['delay'] = data['min_diff'].apply(lambda x: delay(x, threshold=threshold))
        return data

    # ----------------------------------------------------------------
    # Preprocesamiento general
    # ----------------------------------------------------------------
    def preprocess(
        self,
        data: pd.DataFrame,
        target_column: str = None,
        fit: bool = False,
        is_training: bool = False
    ) -> Union[Tuple[pd.DataFrame, pd.Series], pd.DataFrame]:
        """
        - is_training=True  -> se asume que 'Fecha-I' existe y generamos
                               features (period_day, high_season, min_diff)
                               + la columna 'delay'.
        - is_training=False -> no llamamos generate_features() ni add_delay_column().
                               Se espera que el DF ya tenga las col. reales 
                               (OPERA, TIPOVUELO, MES, etc.) para inferir.

        - fit=True  -> ajusta el scaler
        - fit=False -> solo transforma
        """
        logger.info("🔄 Preprocessing data...")

        # SOLO si es entrenamiento generamos las col. basadas en fecha:
        if is_training:
            if 'Fecha-I' not in data.columns:
                raise ValueError("Para entrenamiento, se requiere la columna 'Fecha-I'")

            data = self.generate_features(data)         # crea period_day, etc.
            data = self.add_delay_column(data)          # crea la col. 'delay'

        # target
        target = None
        if target_column and is_training:
            # Separamos la columna target
            target = data[target_column]
            data.drop(columns=[target_column], inplace=True)
            logger.info("✅ Data preprocessed successfully with target column.")

        # One-hot encoding de las col. categóricas que existan
        categorical_columns = ['OPERA', 'TIPOVUELO', 'MES']
        existing_cat_cols = [col for col in categorical_columns if col in data.columns]
        data = pd.get_dummies(data, columns=existing_cat_cols, drop_first=True)

        # Reindex con las features importantes
        data = data.reindex(columns=self._important_features, fill_value=0)

        # Escalado
        if fit:
            self._fitted_columns = data.columns
            data = pd.DataFrame(
                self._scaler.fit_transform(data),
                columns=self._fitted_columns
            )
        else:
            if self._fitted_columns is not None:
                data = data.reindex(columns=self._fitted_columns, fill_value=0)
                data = pd.DataFrame(
                    self._scaler.transform(data),
                    columns=self._fitted_columns
                )
            else:
                raise ValueError("Preprocessing pipeline has not been fitted yet.")
        
        logger.info("✅ Data preprocessed successfully.")
        if target is not None:
            return data, target
        else:
            return data

    # ----------------------------------------------------------------
    # Entrenamiento (fit)
    # ----------------------------------------------------------------
    def fit(self, features: pd.DataFrame, target: pd.Series) -> None:
        """
        Ajusta el modelo con RandomizedSearchCV y guarda 
        los mejores parámetros. Luego entrena con todo 
        (80/20) y exporta a JSON.
        """
        logger.info("🔄 Starting model training with hyperparameter tuning...")

        # Calcula scale_pos_weight
        n_y0 = len(target[target == 0])
        n_y1 = len(target[target == 1])
        scale = n_y0 / n_y1 if n_y1 != 0 else 1
        logger.info(f"🔄 Calculated scale_pos_weight: {scale}")

        param_dist = {
            'n_estimators': [100, 200, 300],
            'learning_rate': [0.01, 0.05, 0.1],
            'max_depth': [3, 5, 6, 8],
            'min_child_weight': [1, 2, 5],
            'gamma': [0, 0.1, 0.2, 0.5],
            'subsample': [0.8, 1.0],
            'colsample_bytree': [0.8, 1.0],
            'scale_pos_weight': [scale]  # Fijamos el scale_pos_weight
        }

        skf = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
        random_search = RandomizedSearchCV(
            estimator=self._model,
            param_distributions=param_dist,
            n_iter=10,  
            scoring='f1',  
            n_jobs=-1,
            cv=skf,
            random_state=42,
            verbose=1
        )
        
        random_search.fit(features, target)
        logger.info(f"🔎 Best params from RandomizedSearchCV: {random_search.best_params_}")

        # Re-entrenar con los mejores parámetros
        best_params = random_search.best_params_
        self._model = XGBClassifier(
            **best_params,
            random_state=42,
            eval_metric='logloss'
        )

        # 80/20 split para validación final
        X_train, X_val, y_train, y_val = train_test_split(
            features, target,
            test_size=0.2,
            random_state=42,
            stratify=target
        )

        self._model.fit(
            X_train, y_train,
            eval_set=[(X_val, y_val)]
        )

        # Guardar modelo en JSON
        self._model.save_model(self._model_json_path)
        # Guardar columnas y scaler
        joblib.dump(self._fitted_columns, self._columns_path)
        joblib.dump(self._scaler, self._scaler_path)

        logger.info("✅ Model trained and saved successfully.")


    def evaluate(self, features: pd.DataFrame, target: pd.Series) -> dict:
        logger.info("🔄 Evaluating the model...")
        predictions = self._model.predict(features)
        evaluation_metrics = {
            'accuracy': accuracy_score(target, predictions),
            'precision': precision_score(target, predictions),
            'recall': recall_score(target, predictions),
            'f1_score': f1_score(target, predictions)
        }
        logger.info(f"✅ Model evaluation completed: {evaluation_metrics}")
        return evaluation_metrics

if __name__ == '__main__':
    model = DelayModel()

    # Carga de datos con fecha, etc. (para entrenamiento)
    data = pd.read_csv('./data/data.csv')
    # Preprocesamos con is_training=True -> generamos period_day, min_diff, etc. + 'delay'
    full_features, full_target = model.preprocess(
        data,
        target_column='delay',
        fit=True,
        is_training=True
    )
    # Entrenamos
    model.fit(full_features, full_target)
    # (Opcional) Evaluamos con todo el set
    metrics = model.evaluate(full_features, full_target)
    logger.info(f"📊 Evaluation Metrics on full data: {metrics}")
    