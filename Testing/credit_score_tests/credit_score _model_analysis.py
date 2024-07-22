import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Parameters
num_farmers = 1000

# Generate synthetic data
np.random.seed(42)  

income_stability = np.random.uniform(0.1, 0.5, num_farmers)  # Coefficient of variation
expense_patterns = np.random.uniform(200, 1000, num_farmers)  # Average monthly expense
yield_consistency = np.random.uniform(10, 50, num_farmers)  # Variance in yield
community_engagement = np.random.randint(0, 10, num_farmers)  # Engagement score (0-10)

# Create DataFrame
data = pd.DataFrame({
    'income_stability': income_stability,
    'expense_patterns': expense_patterns,
    'yield_consistency': yield_consistency,
    'community_engagement': community_engagement
})

data.head(50)

def normalize(value, min_val, max_val):
    return (value - min_val) / (max_val - min_val) * 100

def calculate_credit_score(row):
    # Normalize scores
    income_stability_score = normalize(row['income_stability'], 0, 1)  # Assuming CV ranges from 0 to 1
    expense_patterns_score = normalize(row['expense_patterns'], 0, 1000) 
    yield_consistency_score = normalize(row['yield_consistency'], 0, 100) 
    community_engagement_score = normalize(row['community_engagement'], 0, 10)  

    # Calculate weighted credit score
    credit_score = (0.35 * income_stability_score +
                    0.3 * expense_patterns_score +
                    0.1 * yield_consistency_score +
                    0.25 * community_engagement_score)
    
    return credit_score

data['credit_score'] = data.apply(calculate_credit_score, axis=1)

plt.hist(data['credit_score'], bins=50, edgecolor='k')
plt.title('Distribution of Credit Scores')
plt.xlabel('Credit Score')
plt.ylabel('Number of Farmers')
plt.show()

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Parameters for sensitivity analysis
income_stability_range = np.linspace(0.1, 0.5, 10)
expense_patterns_range = np.linspace(200, 800, 10)
yield_consistency_range = np.linspace(10, 50, 10)
community_engagement_range = np.linspace(0, 10, 10)

def calculate_credit_score(row):
    # Normalize scores
    income_stability_score = normalize(row['income_stability'], 0, 1) 
    expense_patterns_score = normalize(row['expense_patterns'], 0, 1000)  
    yield_consistency_score = normalize(row['yield_consistency'], 0, 100)  
    community_engagement_score = normalize(row['community_engagement'], 0, 10)  

    # Calculate weighted credit score
    credit_score = (0.35 * income_stability_score +
                    0.3 * expense_patterns_score +
                    0.1 * yield_consistency_score +
                    0.25 * community_engagement_score)
    
    return credit_score

# Create synthetic data with sensitivity analysis
sensitivity_data = []
for inc in income_stability_range:
    for exp in expense_patterns_range:
        for yld in yield_consistency_range:
            for com in community_engagement_range:
                sensitivity_data.append({
                    'income_stability': inc,
                    'expense_patterns': exp,
                    'yield_consistency': yld,
                    'community_engagement': com
                })

sensitivity_df = pd.DataFrame(sensitivity_data)
sensitivity_df['credit_score'] = sensitivity_df.apply(calculate_credit_score, axis=1)

# Plot the sensitivity analysis results
plt.hist(sensitivity_df['credit_score'], bins=50, edgecolor='k')
plt.title('Sensitivity Analysis of Credit Scores')
plt.xlabel('Credit Score')
plt.ylabel('Frequency')
plt.show()