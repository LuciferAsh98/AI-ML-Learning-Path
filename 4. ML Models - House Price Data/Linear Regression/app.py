import streamlit as st
import pandas as pd
import joblib
import numpy as np

# Load the model, feature names, and unique locations
model = joblib.load('house_price_model.pkl')
feature_names = joblib.load('feature_names.pkl')
unique_locations = joblib.load('unique_locations.pkl')

# Custom CSS styling
st.markdown("""
    <style>
    .main {
        background-image: url('Images/HeadImage1.webp');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
        color: white;
    }
    .title {
        text-align: center;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: bold;
        margin-top: 20px;
    }
    .description {
        text-align: center;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        margin-bottom: 40px;
    }
    .footer {
        text-align: center;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        margin-top: 40px;
        margin-bottom: 20px;
    }
    .button {
        display: flex;
        justify-content: center;
    }
    .stButton button {
        background-color: #007bff;
        color: white;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 16px;
        border-radius: 4px;
        padding: 10px 20px;
        border: none;
    }
    .stImage img {
        max-width: 80%;
        margin: auto;
        display: block;
    }
    </style>
""", unsafe_allow_html=True)

# Add a header image
st.image("Images/HeadImage1.webp", use_column_width=True)

# Page title
st.markdown('<h1 class="title">Bengaluru House Price Prediction</h1>', unsafe_allow_html=True)

# Add a brief description
st.markdown("""
<p class="description">Welcome to the Bengaluru House Price Prediction app. This tool helps you estimate the price of a house in Bengaluru based on various features such as area, number of bedrooms, bathrooms, balconies, location, and area type.</p>
""", unsafe_allow_html=True)

# Function to get user input
def get_user_input():
    area = st.number_input('Area (sqft)', min_value=0)
    bhk = st.number_input('Number of Bedrooms', min_value=0)
    bath = st.number_input('Number of Bathrooms', min_value=0)
    balcony = st.number_input('Number of Balconies', min_value=0)
    
    location = st.selectbox('Location', unique_locations)
    area_type = st.selectbox('Area Type', ['Super built-up  Area', 'Built-up  Area', 'Plot  Area', 'Carpet  Area'])
    
    # Convert the location and area type to the appropriate dummy variables
    location_dict = {f'location_{loc}': 0 for loc in unique_locations}
    location_dict[f'location_{location}'] = 1
    
    area_type_dict = {f'area_type_{area}': 0 for area in ['Super built-up  Area', 'Built-up  Area', 'Plot  Area', 'Carpet  Area']}
    area_type_dict[f'area_type_{area_type}'] = 1
    
    # Create a DataFrame for the input
    input_data = pd.DataFrame({
        'total_sqft': [area],
        'bhk': [bhk],
        'bath': [bath],
        'balcony': [balcony],
        **location_dict,
        **area_type_dict
    })
    
    # Ensure the DataFrame has the same columns as during training
    for col in feature_names:
        if col not in input_data.columns:
            input_data[col] = 0
    
    input_data = input_data[feature_names]
    
    return input_data

# Get user input
input_data = get_user_input()

# Predict house price
if st.button('Predict'):
    prediction = model.predict(input_data)
    prediction = max(prediction[0], 0)  # Ensure non-negative prediction
    st.write(f'Predicted House Price: ₹{prediction:,.2f}K')

# Add a footer image
st.image("Images/HeadImage2.webp", use_column_width=True)

# Add a closing note
st.markdown("""
<div class="footer">
    Thank you for using our Bengaluru House Price Prediction tool. If you have any questions or feedback, please contact us.
</div>
""", unsafe_allow_html=True)
