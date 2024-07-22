import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

class CreditScoringModel:
    def __init__(self, income_stability_weight=0.3, income_mean_weight=0.3, expense_stability_weight=0.1, expense_mean_weight=0.1, yield_weight=0.15, community_weight=0.05):
        self.weights = {
            'income_stability': income_stability_weight,
            'income_mean': income_mean_weight,
            'expense_stability': expense_stability_weight,
            'expense_mean': expense_mean_weight,
            'yield_consistency': yield_weight,
            'community_engagement': community_weight
        }
        self.model = None

    def normalize(self, value, min_val, max_val):
        clipped_value = np.clip(value, min_val, max_val)
        return (clipped_value - min_val) / (max_val - min_val) * 100

    def calculate_credit_score(self, row):
        # Normalize scores within their respective ranges
        income_stability_score = self.normalize(row['income_stability'], 0, 1)
        income_mean_score = self.normalize(row['income_mean'], 0, 1000)  
        expense_stability_score = self.normalize(row['expense_stability'], 0, 1)
        expense_mean_score = self.normalize(row['expense_mean'], 200, 800)  
        yield_consistency_score = self.normalize(row['yield_consistency'], 0, 100)
        community_engagement_score = self.normalize(row['community_engagement'], 0, 10)
        
        # Calculate the ratio of income to expenses
        income_expense_ratio = row['income_mean'] / row['expense_mean'] if row['expense_mean'] != 0 else 1
        # Penalize the score if expenses are higher than income
        income_expense_penalty = self.normalize(1 - income_expense_ratio, 0, 1)

        # Calculate weighted credit score
        weighted_score = (self.weights['income_stability'] * (100 - income_stability_score) +  
                          self.weights['income_mean'] * income_mean_score +
                          self.weights['expense_stability'] * (100 - expense_stability_score) + 
                          self.weights['expense_mean'] * (100 - expense_mean_score) +  
                          self.weights['yield_consistency'] * (100 - yield_consistency_score) +  
                          self.weights['community_engagement'] * community_engagement_score -  
                          (income_expense_penalty * 100))  

        # Max possible score calculation without the penalty
        max_possible_score = (self.weights['income_stability'] * 100 +
                              self.weights['income_mean'] * 100 +
                              self.weights['expense_stability'] * 100 +
                              self.weights['expense_mean'] * 100 +
                              self.weights['yield_consistency'] * 100 +
                              self.weights['community_engagement'] * 100)

       
        credit_score = (weighted_score / max_possible_score) * 100
        
        return np.clip(credit_score, 0, 100)

    def train_model(self, features, target):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(features, target)

    def feature_importances(self):
        if self.model:
            importances = self.model.feature_importances_
            feature_names = ['income_stability', 'income_mean', 'expense_stability', 'expense_mean', 'yield_consistency', 'community_engagement']
            feature_importances = pd.DataFrame({'feature': feature_names, 'importance': importances})
            return feature_importances.sort_values(by='importance', ascending=False)
        else:
            raise Exception("Model not trained yet")

    def save_model(self, filename):
        if self.model:
            joblib.dump(self.model, filename)
        else:
            raise Exception("Model not trained yet")

    def load_model(self, filename):
        self.model = joblib.load(filename)

    def predict(self, features):
        if self.model:
            return self.model.predict(features)
        else:
            raise Exception("Model not loaded or trained yet")