import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'backend', 'models')))

from fertilizer_recomm_oo import Geocoder, SoilDataFetcher, WeatherDataFetcher, DataPreparer, FertilizerCalculator, FertilizerPredictor

class TestGeocoder(unittest.TestCase):
    """
    Unit tests for the Geocoder class.
    """
    @patch('requests.get')
    def test_geocode_area_name_success(self, mock_get):
        """Test successful geocoding of an area name."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{
            'lat': '1.2345',
            'lon': '2.3456'
        }]
        mock_get.return_value = mock_response

        geocoder = Geocoder()
        result = geocoder.geocode_area_name("Test Area")

        self.assertEqual(result, (1.2345, 2.3456))

    @patch('requests.get')
    def test_geocode_area_name_no_data(self, mock_get):
        """Test geocoding when no data is found for the area name."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        geocoder = Geocoder()
        result = geocoder.geocode_area_name("Test Area")

        self.assertIsNone(result)

    @patch('requests.get')
    def test_geocode_area_name_error(self, mock_get):
        """Test geocoding when an error occurs (e.g., 404 status)."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        geocoder = Geocoder()
        result = geocoder.geocode_area_name("Test Area")

        self.assertIsNone(result)


class TestSoilDataFetcher(unittest.TestCase):
    """
    Unit tests for the SoilDataFetcher class.
    """

    @patch('requests.get')
    def test_fetch_soil_data_success(self, mock_get):
        """Test successful fetching of soil data."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'properties': {
                'layers': [
                    {
                        'name': 'soil',
                        'depths': [
                            {
                                'label': '0-5cm',
                                'values': {
                                    'phh2o_mean': 5.6,
                                    'soc_mean': 2.1
                                }
                            }
                        ]
                    }
                ]
            }
        }
        mock_get.return_value = mock_response

        soil_fetcher = SoilDataFetcher()
        result = soil_fetcher.fetch_soil_data(1.2345, 2.3456)

        expected_data = {
            'soil_0-5cm_phh2o_mean': 5.6,
            'soil_0-5cm_soc_mean': 2.1
        }
        expected_df = pd.DataFrame(expected_data, index=[0])

        pd.testing.assert_frame_equal(result.reset_index(drop=True), expected_df.reset_index(drop=True))

    @patch('requests.get')
    def test_fetch_soil_data_no_properties(self, mock_get):
        """Test fetching soil data when no properties are found."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'properties': {}}
        mock_get.return_value = mock_response

        soil_fetcher = SoilDataFetcher()
        result = soil_fetcher.fetch_soil_data(1.2345, 2.3456)

        self.assertIsNone(result)

    @patch('requests.get')
    def test_fetch_soil_data_error(self, mock_get):
        """Test fetching soil data when an error occurs (e.g., 404 status)."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        soil_fetcher = SoilDataFetcher()
        result = soil_fetcher.fetch_soil_data(1.2345, 2.3456)

        self.assertIsNone(result)


class TestWeatherDataFetcher(unittest.TestCase):
    """
    Unit tests for the WeatherDataFetcher class.
    """

    @patch('requests.get')
    def test_fetch_weather_data_success(self, mock_get):
        """Test successful fetching of weather data."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'current': {
                'temp': 25.0,
                'humidity': 80,
                'rain': {'1h': 1112},
                'uvi': 6
            }
        }
        mock_get.return_value = mock_response

        weather_fetcher = WeatherDataFetcher()
        result = weather_fetcher.fetch_weather_data(1.2345, 2.3456, 'fake_api_key')

        expected_data = {
            'TEMP': 25.0,
            'HUMI': 80,
            'RAIN': 1112,  
            'SUNH': 6
        }

        self.assertEqual(result, expected_data)

    @patch('requests.get')
    def test_fetch_weather_data_auth_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_get.return_value = mock_response

        weather_fetcher = WeatherDataFetcher()
        result = weather_fetcher.fetch_weather_data(1.2345, 2.3456, 'fake_api_key')

        self.assertIsNone(result)

    @patch('requests.get')
    def test_fetch_weather_data_other_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        weather_fetcher = WeatherDataFetcher()
        result = weather_fetcher.fetch_weather_data(1.2345, 2.3456, 'fake_api_key')

        self.assertIsNone(result)


class TestDataPreparer(unittest.TestCase):
    """
    Unit tests for the DataPreparer class.
    """

    def test_prepare_data_for_model_success(self):
        soil_data = {
            'phh2o_0-5cm_mean': [5.6],
            'soc_0-5cm_mean': [2.1],
            'nitrogen_0-5cm_mean': [0.15],
            'cec_0-5cm_mean': [20.0]
        }
        soil_df = pd.DataFrame(soil_data)
        weather_data = {
            'TEMP': 25.0,
            'HUMI': 80.0,
            'RAIN': 5.0,  
            'SUNH': 6.0
        }

        data_preparer = DataPreparer()
        result = data_preparer.prepare_data_for_model(soil_df, weather_data)

        expected_data = {
            'PHAQ': [5.6],
            'TOTC': [2.1],
            'TOTN': [0.15],
            'CECS': [20.0],
            'TEMP': [25.0],
            'RAIN': [5.0],  
            'HUMI': [80.0],
            'SUNH': [6.0]
        }
        expected_df = pd.DataFrame(expected_data)

        pd.testing.assert_frame_equal(result, expected_df)

    def test_prepare_data_for_model_missing_columns(self):
        soil_data = {
            'phh2o_0-5cm_mean': [5.6],
            'soc_0-5cm_mean': [2.1]
        }
        soil_df = pd.DataFrame(soil_data)
        weather_data = {
            'TEMP': 25.0,
            'HUMI': 80,
            'RAIN': 5,
            'SUNH': 6
        }

        data_preparer = DataPreparer()
        result = data_preparer.prepare_data_for_model(soil_df, weather_data)

        self.assertIsNone(result)


class TestFertilizerCalculator(unittest.TestCase):

    def test_calculate_fertilizer_requirements(self):
        yield_prediction = 1000  # kg/ha
        nutrient_coefficients = np.array([1.0, 0.5, 0.2])  # Coefficients for N, P2O5, and K2O per 100 kg of yield
        farm_size_ha = 10

        calculator = FertilizerCalculator()
        result = calculator.calculate_fertilizer_requirements(yield_prediction, nutrient_coefficients, farm_size_ha)

        expected_result = np.array([100.0, 50.0, 20.0])  

        np.testing.assert_array_equal(result, expected_result)


class TestFertilizerPredictor(unittest.TestCase):
    """
    Unit tests for the FertilizerCalculator class.
    """

    @patch.object(Geocoder, 'geocode_area_name')
    @patch.object(SoilDataFetcher, 'fetch_soil_data')
    @patch.object(WeatherDataFetcher, 'fetch_weather_data')
    @patch.object(DataPreparer, 'prepare_data_for_model')
    @patch.object(FertilizerCalculator, 'predict_fertilizer_requirements')
    def test_run(self, mock_predict_fertilizer_requirements, mock_prepare_data_for_model, mock_fetch_weather_data, mock_fetch_soil_data, mock_geocode_area_name):
        mock_geocode_area_name.return_value = (1.2345, 2.3456)
        mock_fetch_soil_data.return_value = pd.DataFrame({
            'phh2o_0-5cm_mean': [5.6],
            'soc_0-5cm_mean': [2.1],
            'nitrogen_0-5cm_mean': [0.15],
            'cec_0-5cm_mean': [20.0]
        })
        mock_fetch_weather_data.return_value = {
            'TEMP': 25.0,
            'HUMI': 80,
            'RAIN': 5,
            'SUNH': 6        }
        mock_prepare_data_for_model.return_value = pd.DataFrame({
            'PHAQ': [5.6],
            'TOTC': [2.1],
            'TOTN': [0.15],
            'CECS': [20.0],
            'TEMP': [25.0],
            'RAIN': [5],
            'HUMI': [80],
            'SUNH': [6]
        })
        mock_predict_fertilizer_requirements.return_value = {
            'Urea (25kg bags)': 4,
            'DAP (25kg bags)': 3,
            'MOP (25kg bags)': 2
        }

        predictor = FertilizerPredictor(area_name="Test Area", api_key="fake_api_key", crop_type="maize", farm_size_acres=10)
        result = predictor.run()

        expected_result = {
            'Urea (25kg bags)': 4,
            'DAP (25kg bags)': 3,
            'MOP (25kg bags)': 2
        }

        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()