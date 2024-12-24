import unittest
import pandas as pd
import numpy as np
from sklearn.exceptions import NotFittedError
from challenge.model import DelayModel


class TestDelayModel(unittest.TestCase):
    def setUp(self):
        """Set up the DelayModel and mock dataset."""
        self.model = DelayModel()
        self.mock_data = pd.DataFrame({
            'Fecha-I': pd.date_range(start='2024-01-01', periods=100, freq='D'),
            'OPERA': ['Grupo LATAM'] * 50 + ['Sky Airline'] * 50,
            'TIPOVUELO': ['I'] * 100,
            'MES': [1, 2, 3, 4, 5] * 20,
            'min_diff': np.random.randint(-30, 120, 100)
        })

    def test_generate_features(self):
        """Test the generate_features method."""
        processed_data = self.model.generate_features(self.mock_data.copy())
        self.assertIn('period_day', processed_data.columns)
        self.assertIn('high_season', processed_data.columns)
        self.assertIn('min_diff', processed_data.columns)

    def test_add_delay_column(self):
        """Test the add_delay_column method."""
        data = self.mock_data.copy()
        data['min_diff'] = [-10, 20, 5, 30, 0] * 20
        processed_data = self.model.add_delay_column(data, threshold=15)
        self.assertIn('delay', processed_data.columns)
        self.assertEqual(set(processed_data['delay'].unique()), {0, 1})

    def test_preprocess_training(self):
        """Test the preprocess method during training."""
        data = self.mock_data.copy()
        features, target = self.model.preprocess(data, target_column='delay', fit=True, is_training=True)
        self.assertIsInstance(features, pd.DataFrame)
        self.assertIsInstance(target, pd.Series)
        self.assertEqual(features.shape[1], len(self.model._important_features))
        self.assertEqual(len(target), len(features))

    def test_preprocess_inference(self):
        """Test the preprocess method during inference."""
        data = self.mock_data.copy()
        
        # Preprocessing for training to fit the pipeline
        data = self.model.generate_features(data)
        data = self.model.add_delay_column(data)
        features, target = self.model.preprocess(data, target_column='delay', fit=True, is_training=True)
        
        # Inference preprocessing
        inference_data = self.mock_data.copy()
        inference_data = self.model.generate_features(inference_data)
        inference_data = self.model.add_delay_column(inference_data)
    
        # Preprocess without fitting again
        features = self.model.preprocess(inference_data, is_training=False)
        
        self.assertIsInstance(features, pd.DataFrame)
        self.assertEqual(features.shape[1], len(self.model._important_features))


    def test_preprocess_error(self):
        """Test preprocess without fitting."""
        with self.assertRaises(ValueError):
            self.model.preprocess(self.mock_data, is_training=False)

    def test_fit(self):
        """Test the fit method."""
        data = self.mock_data.copy()
        data = self.model.generate_features(data)
        data = self.model.add_delay_column(data)
        features, target = self.model.preprocess(data, target_column='delay', fit=True, is_training=True)
        self.model.fit(features, target)
        self.assertTrue(hasattr(self.model._model, 'feature_importances_'))

    def test_evaluate(self):
        """Test the evaluate method."""
        data = self.mock_data.copy()
        data = self.model.generate_features(data)
        data = self.model.add_delay_column(data)
        features, target = self.model.preprocess(data, target_column='delay', fit=True, is_training=True)
        self.model.fit(features, target)
        metrics = self.model.evaluate(features, target)
        self.assertIsInstance(metrics, dict)
        self.assertIn('accuracy', metrics)
        self.assertIn('precision', metrics)
        self.assertIn('recall', metrics)
        self.assertIn('f1_score', metrics)

    def test_predict(self):
        """Test predictions after fitting."""
        data = self.mock_data.copy()
        data = self.model.generate_features(data)
        data = self.model.add_delay_column(data)
        features, target = self.model.preprocess(data, target_column='delay', fit=True, is_training=True)
        self.model.fit(features, target)
        predictions = self.model._model.predict(features)
        self.assertEqual(len(predictions), len(features))
        self.assertTrue(all(pred in [0, 1] for pred in predictions))

    def test_predict_without_fit(self):
        """Test prediction error without fitting."""
        with self.assertRaises(NotFittedError):
            self.model._model.predict(pd.DataFrame(np.random.rand(10, len(self.model._important_features))))

    def test_preprocess_missing_column(self):
        """Test preprocess error with missing Fecha-I column."""
        incomplete_data = self.mock_data.drop(columns=['Fecha-I'])
        with self.assertRaises(ValueError):
            self.model.preprocess(incomplete_data, is_training=True)


if __name__ == '__main__':
    unittest.main()
