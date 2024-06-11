import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score
import joblib

# Load the dataset
file_path = 'bengaluru_house_prices.csv'
data = pd.read_csv(file_path)

# Data preprocessing
# Dropping unnecessary columns
data = data.drop(['society', 'availability'], axis='columns')

# Handling missing values
data = data.dropna()
data['bhk'] = data['size'].apply(lambda x: int(x.split(' ')[0]))

# Convert total_sqft to a numerical value
def convert_sqft_to_num(x):
    tokens = x.split('-')
    if len(tokens) == 2:
        return (float(tokens[0]) + float(tokens[1])) / 2
    try:
        return float(x)
    except:
        return None

data['total_sqft'] = data['total_sqft'].apply(convert_sqft_to_num)
data = data[data['total_sqft'].notnull()]

# Removing outliers
data = data[~(data.total_sqft / data.bhk < 300)]
data['price_per_sqft'] = data['price'] * 100000 / data['total_sqft']

# Location preprocessing
data.location = data.location.apply(lambda x: x.strip())
location_stats = data.groupby('location')['location'].agg('count').sort_values(ascending=False)
location_stats_less_than_10 = location_stats[location_stats <= 10]
data.location = data.location.apply(lambda x: 'other' if x in location_stats_less_than_10 else x)

# Save unique locations
unique_locations = data['location'].unique().tolist()
with open('unique_locations.pkl', 'wb') as f:
    joblib.dump(unique_locations, f)

# Removing more outliers
def remove_pps_outliers(df):
    df_out = pd.DataFrame()
    for key, subdf in df.groupby('location'):
        m = np.mean(subdf.price_per_sqft)
        st = np.std(subdf.price_per_sqft)
        reduced_df = subdf[(subdf.price_per_sqft > (m - st)) & (subdf.price_per_sqft <= (m + st))]
        df_out = pd.concat([df_out, reduced_df], ignore_index=True)
    return df_out

data = remove_pps_outliers(data)

# Remove BHK outliers
def remove_bhk_outliers(df):
    exclude_indices = np.array([])
    for location, location_df in df.groupby('location'):
        bhk_stats = {}
        for bhk, bhk_df in location_df.groupby('bhk'):
            bhk_stats[bhk] = {
                'mean': np.mean(bhk_df.price_per_sqft),
                'std': np.std(bhk_df.price_per_sqft),
                'count': bhk_df.shape[0]
            }
        for bhk, bhk_df in location_df.groupby('bhk'):
            stats = bhk_stats.get(bhk - 1)
            if stats and stats['count'] > 5:
                exclude_indices = np.append(exclude_indices, bhk_df[bhk_df.price_per_sqft < (stats['mean'])].index.values)
    return df.drop(exclude_indices, axis='index')

data = remove_bhk_outliers(data)

# Final clean up
data = data[data.bath < data.bhk + 2]
data = data.drop(['size', 'price_per_sqft'], axis='columns')

# Encoding categorical data
data = pd.get_dummies(data, columns=['location', 'area_type'], drop_first=True)

# Split data into features and target
X = data.drop('price', axis=1)
y = data['price']

# Save feature names
feature_names = X.columns.tolist()
with open('feature_names.pkl', 'wb') as f:
    joblib.dump(feature_names, f)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=10)

# Create a pipeline with Polynomial Features and Ridge Regression
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('poly', PolynomialFeatures(degree=2, include_bias=False)),
    ('ridge', Ridge(alpha=1.0))
])

# Train the model
pipeline.fit(X_train, y_train)

# Predict and evaluate the model
y_pred = pipeline.predict(X_test)
r2 = r2_score(y_test, y_pred)
print(f'R2 Score: {r2}')

# Save the trained model
joblib.dump(pipeline, 'house_price_model.pkl')
