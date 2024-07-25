import os
import streamlit as st
import pandas as pd
import openai
from dotenv import load_dotenv
from streamlit_chat import message

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Title of the Streamlit app
st.title("PropBot - Your Real Estate Chatbot")
st.write("Hey, my name is PropBot from Zummit. What can I help you with today?")

# Load the datasets
land_data = pd.read_csv('land_api_responses.csv')
residential_data = pd.read_csv('res_api_responses.csv')

# Data cleaning: strip any leading/trailing spaces from column names
land_data.columns = land_data.columns.str.strip()
residential_data.columns = residential_data.columns.str.strip()

# Function to filter properties based on user input
def filter_properties(location, rooms, sector):
    location_lower = location.strip().lower()
    sector_lower = sector.strip().lower()
    
    matched_land_properties = land_data[
        (land_data['Area'].str.lower() == location_lower) &
        (land_data['Sector'].str.lower() == sector_lower)
    ]
    
    matched_residential_properties = residential_data[
        (residential_data['Area'].str.lower() == location_lower) &
        (residential_data['Residential No of Rooms'].astype(str) == str(rooms)) &
        (residential_data['Sector'].str.lower() == sector_lower)
    ]
    
    matched_properties = pd.concat([matched_land_properties, matched_residential_properties])
    
    return matched_properties

# Combine unique sectors and locations from both datasets
combined_sectors = pd.concat([land_data['Sector'], residential_data['Sector']]).unique()
combined_locations = pd.concat([land_data['Area'], residential_data['Area']]).unique()
combined_rooms = sorted(residential_data['Residential No of Rooms'].unique())

# Streamlit interface for property filters
location = st.selectbox('Select Location', sorted(combined_locations), key='location')
rooms = st.selectbox('Select Number of Rooms', combined_rooms, key='rooms')
sector = st.selectbox('Select Sector', sorted(combined_sectors), key='sector')

matched_properties = pd.DataFrame()  # Initialize as an empty DataFrame

if st.button('Get Properties'):
    matched_properties = filter_properties(location, rooms, sector)
    st.session_state.matched_properties = matched_properties
    
    if not matched_properties.empty:
        response = f"Here are the properties in {location}:\n"
        for index, row in matched_properties.iterrows():
            response += f"ID: {index}\nSector: {row['Sector']}\nNo of Rooms: {row.get('Residential No of Rooms', 'N/A')}\nSales Cost: {row['Sales Cost (Local)']}\nRent Cost: {row.get('Rents Cost (Local)', 'N/A')}\n\n"
        st.write(response.strip())
    else:
        st.write(f"Sorry, no properties found in {location} with {rooms} rooms in {sector} sector.")
else:
    st.session_state.matched_properties = pd.DataFrame()  # Initialize as an empty DataFrame

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input and response generation
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

