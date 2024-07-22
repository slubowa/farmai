import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
import joblib

# Load the combined dataset
df = pd.read_csv('../data/soil_climate_yield_data.csv')

# Features for modeling
features = ['PHAQ', 'TOTC', 'TOTN', 'CECS','TEMP', 'RAIN', 'HUMI', 'SUNH']
X = df[features]
y_maize = df['Estimated_Maize_Yield']
y_cassava = df['Estimated_Cassava_Yield']
y_beans = df['Estimated_Beans_Yield']

# Split the data into training and testing sets
X_train_maize, X_test_maize, y_train_maize, y_test_maize = train_test_split(X, y_maize, test_size=0.2, random_state=42)
X_train_cassava, X_test_cassava, y_train_cassava, y_test_cassava = train_test_split(X, y_cassava, test_size=0.2, random_state=42)
X_train_beans, X_test_beans, y_train_beans, y_test_beans = train_test_split(X, y_beans, test_size=0.2, random_state=42)

# Initialize the models
model_maize = RandomForestRegressor(n_estimators=100, random_state=42)
model_cassava = RandomForestRegressor(n_estimators=100, random_state=42)
model_beans = RandomForestRegressor(n_estimators=100, random_state=42)

# Train the models
model_maize.fit(X_train_maize, y_train_maize)
model_cassava.fit(X_train_cassava, y_train_cassava)
model_beans.fit(X_train_beans, y_train_beans)

# Save the models
joblib.dump(model_maize, 'model_maize.joblib')
joblib.dump(model_cassava, 'model_cassava.joblib')
joblib.dump(model_beans, 'model_beans.joblib')

# Predict on the test set
y_pred_maize = model_maize.predict(X_test_maize)
y_pred_cassava = model_cassava.predict(X_test_cassava)
y_pred_beans = model_beans.predict(X_test_beans)

# Evaluate the models
mse_maize = mean_squared_error(y_test_maize, y_pred_maize)
mae_maize = mean_absolute_error(y_test_maize, y_pred_maize)
r2_maize = r2_score(y_test_maize, y_pred_maize)

mse_beans = mean_squared_error(y_test_beans, y_pred_beans)
mae_beans = mean_absolute_error(y_test_beans, y_pred_beans)
r2_beans = r2_score(y_test_beans, y_pred_beans)

mse_cassava = mean_squared_error(y_test_cassava, y_pred_cassava)
mae_cassava = mean_absolute_error(y_test_cassava, y_pred_cassava)
r2_cassava = r2_score(y_test_cassava, y_pred_cassava)

# Print evaluation metrics
print(f'Mean Squared Error for Maize: {mse_maize}')
print(f'Mean Absolute Error for Maize: {mae_maize}')
print(f'R2 Score for Maize: {r2_maize}')

print(f'Mean Squared Error for Cassava: {mse_cassava}')
print(f'Mean Absolute Error for Cassava: {mae_cassava}')
print(f'R2 Score for Cassava: {r2_cassava}')

print(f'Mean Squared Error for Beans: {mse_beans}')
print(f'Mean Absolute Error for Beans: {mae_beans}')
print(f'R2 Score for Beans: {r2_beans}')