import unittest
from unittest.mock import patch, MagicMock
import numpy as np
import pandas as pd
import sys
import os
from sklearn.ensemble import RandomForestRegressor
import joblib
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'backend', 'models')))
from credit_scoring_model import CreditScoringModel

class TestCreditScoringModel(unittest.TestCase):

    def setUp(self):
        """Set up the initial conditions for the tests"""
        self.model = CreditScoringModel()
        self.row = {
            'income_stability': 0.8,
            'income_mean': 500,
            'expense_stability': 0.3,
            'expense_mean': 400,
            'yield_consistency': 50,
            'community_engagement': 7
        }
        self.features = pd.DataFrame([self.row])
        self.target = pd.Series([75])

    def test_normalize(self):
        """ Test the normalize method with various inputs """
        self.assertEqual(self.model.normalize(0.5, 0, 1), 50)
        self.assertEqual(self.model.normalize(100, 0, 200), 50)
        self.assertEqual(self.model.normalize(300, 200, 800), 16.666666666666664)
        self.assertEqual(self.model.normalize(900, 0, 1000), 90)
        self.assertEqual(self.model.normalize(-10, 0, 100), 0)
        self.assertEqual(self.model.normalize(110, 0, 100), 100)

    def test_calculate_credit_score(self):
        """Test the calculate_credit_score method to ensure the score is within 0 and 100"""
        score = self.model.calculate_credit_score(self.row)
        self.assertTrue(0 <= score <= 100)

    def test_train_model(self):
        """Test the train_model method to ensure the model is trained"""
        self.model.train_model(self.features, self.target)
        self.assertIsInstance(self.model.model, RandomForestRegressor)

    def test_feature_importances(self):
        """Test the feature_importances method to ensure it returns 
        a DataFrame of feature importances"""
        self.model.train_model(self.features, self.target)
        importances = self.model.feature_importances()
        self.assertIsInstance(importances, pd.DataFrame)
        self.assertEqual(len(importances), 6)

    def test_save_and_load_model(self):
        """Test the save_model and load_model methods to 
        ensure the model can be saved and loaded correctly"""
        self.model.train_model(self.features, self.target)
        self.model.save_model('test_model.joblib')
        self.model.load_model('test_model.joblib')
        self.assertIsInstance(self.model.model, RandomForestRegressor)
        os.remove('test_model.joblib')

    def test_predict(self):
        """Test the predict method to ensure it returns predictions"""
        self.model.train_model(self.features, self.target)
        predictions = self.model.predict(self.features)
        self.assertEqual(len(predictions), 1)

    @patch('joblib.dump')
    def test_save_model_exception(self, mock_dump):
        """Test the save_model method to ensure it raises an exception
        for an untrained model"""
        model = CreditScoringModel()
        with self.assertRaises(Exception):
            model.save_model('test_model.joblib')

    @patch('joblib.load')
    def test_load_model(self, mock_load):
        """Test the load_model method to ensure it correctly loads 
        the model using a mock"""
        mock_model = RandomForestRegressor()
        mock_load.return_value = mock_model
        self.model.load_model('test_model.joblib')
        self.assertIsInstance(self.model.model, RandomForestRegressor)

    def test_predict_exception(self):
        """Test the predict method to ensure it raises an 
        exception for an untrained or unloaded model"""
        model = CreditScoringModel()
        with self.assertRaises(Exception):
            model.predict(self.features)

if __name__ == '__main__':
    unittest.main()