import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error

# Read the data
data = pd.read_csv("kc_house_data.csv")

# Display the first few rows and summary statistics
print(data.head())
print(data.describe())

# Visualizations
plt.figure(figsize=(10, 5))
sns.histplot(data['price'], bins=50, kde=True)
plt.title('Distribution of House Prices')
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.show()

plt.figure(figsize=(10, 5))
sns.scatterplot(x=data['sqft_living'], y=data['price'])
plt.title('Price vs Square Feet')
plt.xlabel('Square Feet')
plt.ylabel('Price')
plt.show()

plt.figure(figsize=(10, 5))
sns.boxplot(x=data['bedrooms'], y=data['price'])
plt.title('Price vs Number of Bedrooms')
plt.xlabel('Number of Bedrooms')
plt.ylabel('Price')
plt.show()

plt.figure(figsize=(10, 5))
sns.scatterplot(x=data['lat'], y=data['long'], hue=data['price'], palette='viridis')
plt.title('Geographical Price Distribution')
plt.xlabel('Latitude')
plt.ylabel('Longitude')
plt.show()

# Assume that columns 'income', 'schools', 'hospitals', and 'crime_rate' exist in the dataset
factors = ['income', 'schools', 'hospitals', 'crime_rate']

# Prepare the data for modeling
labels = data['price']
features = data[factors + ['sqft_living', 'bedrooms', 'bathrooms', 'lat', 'long', 'waterfront', 'condition']]

# Split the data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(features, labels, test_size=0.10, random_state=2)

# Train an XGBoost model
xgboost_model = XGBRegressor(n_estimators=400, max_depth=5, learning_rate=0.1, objective='reg:squarederror')
xgboost_model.fit(x_train, y_train)
y_pred = xgboost_model.predict(x_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
print("XGBoost Mean Squared Error:", mse)
print("XGBoost Score:", xgboost_model.score(x_test, y_test))

# Visualize the feature importance
plt.figure(figsize=(10, 5))
importance = xgboost_model.feature_importances_
sorted_idx = np.argsort(importance)
plt.barh(features.columns[sorted_idx], importance[sorted_idx])
plt.title('Feature Importance')
plt.xlabel('Importance')
plt.ylabel('Features')
plt.show()

# PCA (Optional: for dimensionality reduction, not directly related to the main prediction task)
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)
pca = PCA(n_components=2)  # Example to reduce to 2 components
pca_components = pca.fit_transform(scaled_features)

plt.figure(figsize=(10, 5))
plt.scatter(pca_components[:, 0], pca_components[:, 1], c=labels, cmap='viridis')
plt.title('PCA of Home Prices')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.colorbar(label='Price')
plt.show()
