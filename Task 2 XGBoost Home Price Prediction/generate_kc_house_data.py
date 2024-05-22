import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Generate sample data
num_rows = 1000
data = {
    'price': np.random.randint(100000, 1000000, size=num_rows),
    'income': np.random.randint(30000, 150000, size=num_rows),
    'schools': np.random.randint(1, 10, size=num_rows),
    'hospitals': np.random.randint(1, 10, size=num_rows),
    'crime_rate': np.random.rand(num_rows) * 100,
    'sqft_living': np.random.randint(500, 6000, size=num_rows),
    'bedrooms': np.random.randint(1, 6, size=num_rows),
    'bathrooms': np.random.randint(1, 4, size=num_rows),
    'lat': np.random.uniform(47.5, 47.8, size=num_rows),
    'long': np.random.uniform(-122.5, -122.2, size=num_rows),
    'waterfront': np.random.randint(0, 2, size=num_rows),
    'condition': np.random.randint(1, 5, size=num_rows)
}

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv("kc_house_data.csv", index=False)

print("CSV file 'kc_house_data.csv' created successfully!")
