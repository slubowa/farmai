import numpy as np
import pandas as pd
import joblib
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(project_root)

from backend.models.credit_scoring_model import CreditScoringModel 

def calculate_variances(values):
    mean = np.mean(values)
    variance = np.var(values)
    stability = np.std(values) / mean if mean != 0 else 0
    return mean, variance, stability

def generate_synthetic_data(n):
    """ Function to generate synthetic data for the features"""
    income_data = np.random.uniform(500, 2000, n)
    expense_data = np.random.uniform(200, 800, n)
    yield_data = np.random.uniform(10, 50, n)
    community_data = np.random.randint(0, 10, n)
    
    data = pd.DataFrame({
        'income_stability': np.random.uniform(0.1, 0.5, n),
        'income_mean': income_data,
        'expense_stability': np.random.uniform(0.1, 0.5, n),
        'expense_mean': expense_data,
        'yield_consistency': np.random.uniform(10, 50, n),
        'community_engagement': community_data
    })
    
    return data

def train_credit_scoring():
    # Generate synthetic data
    data = generate_synthetic_data(1000)

    # Initialize model
    model = CreditScoringModel()

    # Calculate credit scores
    data['credit_score'] = data.apply(model.calculate_credit_score, axis=1)

    print(data[['income_stability', 'income_mean', 'expense_stability', 'expense_mean', 'yield_consistency', 'community_engagement', 'credit_score']].head())

    # Train the model
    features = data[['income_stability', 'income_mean', 'expense_stability', 'expense_mean', 'yield_consistency', 'community_engagement']]
    target = data['credit_score']
    model.train_model(features, target)

    # feature importances
    print(model.feature_importances())

    # Save the trained model
    model_dir = os.path.join(project_root, 'backend', 'models')
    model_path = os.path.join(model_dir, 'credit_scoring_model.pkl')
    model.save_model(model_path)
    print(f'Model saved to {model_path}')

if __name__ == '__main__':
    train_credit_scoring()