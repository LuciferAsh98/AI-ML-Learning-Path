import streamlit as st
import pandas as pd
import joblib
import numpy as np

# Load the model, feature names, and unique locations
model = joblib.load('house_price_model.pkl')
feature_names = joblib.load('feature_names.pkl')
unique_locations = joblib.load('unique_locations.pkl')

st.title('Bengaluru House Price Prediction')

# Function to get user input
def get_user_input():
    area = st.number_input('Area (sqft)', min_value=0)
    bhk = st.number_input('Number of Bedrooms', min_value=0)
    bath = st.number_input('Number of Bathrooms', min_value=0)
    
    location = st.selectbox('Location', unique_locations)
    
    # Convert the location to the appropriate dummy variables
    location_dict = {f'location_{loc}': 0 for loc in unique_locations}
    location_dict[f'location_{location}'] = 1
    
    # Create a DataFrame for the input
    input_data = pd.DataFrame({
        'total_sqft': [area],
        'bhk': [bhk],
        'bath': [bath],
        **location_dict
    })
    
    # Ensure the DataFrame has the same columns as during training
    for col in feature_names:
        if col not in input_data.columns:
            input_data[col] = 0
    
    input_data = input_data[feature_names]
    
    return input_data

# Get user input
input_data = get_user_input()

# Display the input features
st.write('Input Features:')
st.write(input_data)

# Predict house price
if st.button('Predict'):
    prediction = model.predict(input_data)
    st.write(f'Predicted House Price: ₹{prediction[0]:,.2f}')
