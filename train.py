from sklearn.datasets import fetch_california_housing
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import pandas as pd
import joblib

# Load the California housing dataset
data = fetch_california_housing()

# Convert the dataset to a pandas DataFrame
x = pd.DataFrame(data.data, columns=data.feature_names)
y = data.target

print("Features shape:", x.shape[0])
print("Target shape:", y.shape[0])

# Split the dataset into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Create a Random Forest Regressor model
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Train the model
model.fit(x_train, y_train)

# Make predictions on the test set
y_pred = model.predict(x_test)

# Evaluate the model
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Absolute Error: ${mae* 100000:,.4f}")
print(f"R-squared Score: {r2:.4f}")

# Save the trained model
joblib.dump(model, "house_model.joblib")
joblib.dump(list(x.columns), "house_features.joblib")
