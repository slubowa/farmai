import requests
import pandas as pd
import numpy as np
import logging
from time import sleep
import joblib
import os
import math
from sklearn.impute import SimpleImputer

#logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Geocoder:
    """
    Class responsible for geocoding area names to coordinates using the Nominatim API.
    """
    @staticmethod
    def geocode_area_name(area_name):
        """
        Geocode an area name to its latitude and longitude coordinates.
        """
        api_url = f'https://nominatim.openstreetmap.org/search?q={area_name}&format=json'
        headers = {
            'User-Agent': 'Mozilla/5.0'
        }
        response = requests.get(api_url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if data:
                location = data[0]
                latitude = float(location['lat'])
                longitude = float(location['lon'])
                return latitude, longitude
            else:
                logging.error("No location found for the given area name.")
                return None
        else:
            logging.error(f"Error: {response.status_code}")
            return None


class SoilDataFetcher:
    """
    Class responsible for fetching soil data from the SoilGrids API.
    """
    def fetch_soil_data(self, latitude, longitude, radius=0.5, max_attempts=10, step=0.05):
        """
        Fetch soil data for a given latitude and longitude, with a specified search radius and max attempts.
        """
        attempt = 0
        
        lat_shifts = np.arange(-radius, radius + step, step)
        lon_shifts = np.arange(-radius, radius + step, step)
        
        total_attempts = min(max_attempts, len(lat_shifts) * len(lon_shifts))
        
        for lat_shift in lat_shifts:
            for lon_shift in lon_shifts:
                if attempt >= total_attempts:
                    break
                attempt += 1
                lat_attempt = latitude + lat_shift
                lon_attempt = longitude + lon_shift
                
                api_url = f'https://rest.isric.org/soilgrids/v2.0/properties/query?lon={lon_attempt}&lat={lat_attempt}'
                response = requests.get(api_url)
                
                if response.status_code == 200:
                    soil_data = response.json()
                    logging.info(f"Attempt {attempt}: Coordinates ({lat_attempt}, {lon_attempt})")
                    
                    properties = soil_data.get('properties', {}).get('layers', [])
                    if properties:
                        soil_properties = {}
                        for layer in properties:
                            layer_name = layer.get('name', 'unknown')
                            for depth in layer.get('depths', []):
                                label = depth.get('label', 'unknown')
                                values = depth.get('values', {})
                                for key, value in values.items():
                                    soil_properties[f"{layer_name}_{label}_{key}"] = value
                        
                        df = pd.DataFrame.from_dict(soil_properties, orient='index', columns=['value'])
                        df = df.T  # Transpose to make sure the columns are as expected
                        return df
                    else:
                        logging.warning("No properties found in the response.")
                else:
                    logging.error(f"Error: {response.status_code}")
                    sleep(1)  # Wait a bit before the next attempt

        logging.error("Max attempts reached, no valid data found.")
        return None


class WeatherDataFetcher:
    """
    Class responsible for fetching weather data from the OpenWeatherMap API.
    """
    def fetch_weather_data(self, latitude, longitude, api_key):
        """
        Fetch weather data for a given latitude and longitude using an API key.
        """
        api_url = f'http://api.openweathermap.org/data/3.0/onecall?lat={latitude}&lon={longitude}&appid={api_key}&units=metric'
        response = requests.get(api_url)
        
        if response.status_code == 200:
            weather_data = response.json()
            logging.info("API key works. Here is the data:")
            logging.info(weather_data)
            
            current = weather_data.get('current', {})
            temp = current.get('temp')
            humidity = current.get('humidity')
            rain = current.get('rain', {}).get('1h', 0)  # Assuming rain data is in mm
            sunh = current.get('uvi', 0)  # Using UV index as a proxy for sunlight hours
            
            # Adjust for low or zero rain values
            if rain < 10:
                rain = 1112  # Use average value

            return {
                'TEMP': temp,
                'HUMI': humidity,
                'RAIN': rain,
                'SUNH': sunh
            }
        elif response.status_code == 401:
            logging.error("Authentication error: Please check your API key.")
        else:
            logging.error(f"Error: {response.status_code}")
        return None


class DataPreparer:
    """
    Class responsible for preparing data for model input.
    """
    @staticmethod
    def prepare_data_for_model(soil_df, weather_data):
        """
        Prepare and clean data to be used as input for the fertilizer recommendation model.
        """
        relevant_columns = {
            'phh2o_0-5cm_mean': 'PHAQ',
            'soc_0-5cm_mean': 'TOTC',
            'nitrogen_0-5cm_mean': 'TOTN',
            'cec_0-5cm_mean': 'CECS'
        }
        
        missing_columns = [col for col in relevant_columns.keys() if col not in soil_df.columns]
        if missing_columns:
            logging.error(f"Missing columns in the fetched data: {missing_columns}")
            return None
        
        prepared_df = soil_df[relevant_columns.keys()].rename(columns=relevant_columns)
        
        for key, value in weather_data.items():
            prepared_df[key] = value
        
        # Handling NaN values by replacing them with the mean of the column
        imputer = SimpleImputer(strategy='mean')
        prepared_df = pd.DataFrame(imputer.fit_transform(prepared_df), columns=prepared_df.columns)

        # Reordering the columns to match the order during model training
        feature_order = ['PHAQ', 'TOTC', 'TOTN', 'CECS','TEMP', 'RAIN', 'HUMI', 'SUNH']
        prepared_df = prepared_df[feature_order]
        
        return prepared_df


class FertilizerCalculator:
    """
    Class responsible for calculating fertilizer requirements.
    """
    @staticmethod
    def calculate_fertilizer_requirements(yield_prediction, nutrient_coefficients, farm_size_ha):
        """
        Calculate fertilizer requirements based on predicted yield and nutrient coefficients.
        """
        nutrient_requirements_per_ha = yield_prediction * nutrient_coefficients / 100
        nutrient_requirements_total = nutrient_requirements_per_ha * farm_size_ha
        logging.info(f"Nutrient requirements per ha: {nutrient_requirements_per_ha}")
        logging.info(f"Total nutrient requirements: {nutrient_requirements_total}")
        return nutrient_requirements_total

    def predict_fertilizer_requirements(self, prepared_df, crop_type, farm_size_acres):
        # Convert farm size from acres to hectares
        farm_size_ha = farm_size_acres * 0.404686
        
        base_path = os.path.dirname(__file__)  
        model_path = os.path.join(base_path, '..', 'training')


        if crop_type.lower() == 'maize':
            model = joblib.load(os.path.join(model_path, 'model_maize.joblib'))
        elif crop_type.lower() == 'cassava':
            model = joblib.load(os.path.join(model_path, 'model_cassava.joblib'))
        elif crop_type.lower() == 'beans':
            model = joblib.load(os.path.join(model_path, 'model_beans.joblib'))
        else:
            logging.error("Invalid crop type. Please choose from 'maize', 'cassava', or 'beans'.")
            return None
        
        yield_prediction = model.predict(prepared_df)
        logging.info(f"Predicted yield: {yield_prediction[0]} kg/ha")
        
        nutrient_coefficients = np.array([1.0, 0.5, 0.2])  # Coefficients for N, P2O5, and K2O per 100 kg of yield

        # Calculate nutrient requirements based on predicted yield
        nutrient_requirements = self.calculate_fertilizer_requirements(yield_prediction[0], nutrient_coefficients, farm_size_ha)
        
        # Fertilizer products and their nutrient contents
        fertilizers = {
            'Urea (25kg bags)': {'N': 0.46},
            'DAP (25kg bags)': {'N': 0.18, 'P2O5': 0.46},
            'MOP (25kg bags)': {'K2O': 0.60}
        }
        
        fertilizer_bags = {
            'Urea (25kg bags)': 0,
            'DAP (25kg bags)': 0,
            'MOP (25kg bags)': 0
        }

        # Calculate the number of bags required for each fertilizer
        # Calculate nitrogen from Urea
        fertilizer_bags['Urea (25kg bags)'] = math.ceil(nutrient_requirements[0] / fertilizers['Urea (25kg bags)']['N'] / 25)
        # Calculate phosphorus from DAP
        fertilizer_bags['DAP (25kg bags)'] = math.ceil(nutrient_requirements[1] / fertilizers['DAP (25kg bags)']['P2O5'] / 25)
        # Calculate potassium from MOP
        fertilizer_bags['MOP (25kg bags)'] = math.ceil(nutrient_requirements[2] / fertilizers['MOP (25kg bags)']['K2O'] / 25)

        return fertilizer_bags


class FertilizerPredictor:
    """
        Class to predict the fertilizer requirements for a specific 
        crop type and farm size."""
    def __init__(self, area_name, api_key, crop_type, farm_size_acres):
        self.area_name = area_name
        self.api_key = api_key
        self.crop_type = crop_type
        self.farm_size_acres = farm_size_acres

    def run(self):
        geocoder = Geocoder()
        soil_fetcher = SoilDataFetcher()
        weather_fetcher = WeatherDataFetcher()
        data_preparer = DataPreparer()
        fertilizer_calculator = FertilizerCalculator()

        coordinates = geocoder.geocode_area_name(self.area_name)
        
        if coordinates:
            latitude, longitude = coordinates
            logging.info(f"Coordinates for {self.area_name}: Latitude = {latitude}, Longitude = {longitude}")
            soil_df = soil_fetcher.fetch_soil_data(latitude, longitude)
            if soil_df is not None:
                logging.info(f"Fetched soil data:\n{soil_df}")
                weather_data = weather_fetcher.fetch_weather_data(latitude, longitude, self.api_key)
                
                if weather_data:
                    prepared_df = data_preparer.prepare_data_for_model(soil_df, weather_data)
                    
                    if prepared_df is not None:
                        fertilizer_requirement = fertilizer_calculator.predict_fertilizer_requirements(prepared_df, self.crop_type, self.farm_size_acres)
                        if fertilizer_requirement is not None:
                            logging.info(f"Fertilizer requirement for {self.farm_size_acres} acres of {self.crop_type}: {fertilizer_requirement}")
                    else:
                        logging.error("Failed to prepare data for the model.")
                else:            
                    logging.error("Failed to fetch weather data.")
            else:
                logging.error("Failed to fetch soil data.")
        else:
            logging.error("Failed to fetch coordinates for the area.")

        return fertilizer_requirement