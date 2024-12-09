import streamlit as st
import pandas as pd
import pickle
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Load Random Forest Model
with open('random_forest_model.pkl', 'rb') as file:
    random_forest_model = pickle.load(file)

# Load Dataset
avocado_data = pd.read_csv('Avocado_Prices_Data.csv')

# Preprocessor
numerical_cols = ['TotalVolume', 'plu4046', 'plu4225', 'plu4770', 'TotalBags', 'SmallBags', 'LargeBags', 'XLargeBags']
categorical_cols = ['type', 'region']

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_cols),
        ('cat', OneHotEncoder(drop='first', handle_unknown='ignore'), categorical_cols)
    ]
)

# Registration and Login
users = {"admin": "password"}  # Simple hardcoded user dictionary

def main():
    st.title("Avocado Price Prediction App")
    
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    
    if not st.session_state['authenticated']:
        st.sidebar.title("User Authentication")
        action = st.sidebar.radio("Choose Action", ["Login", "Register"])
        
        if action == "Register":
            st.sidebar.header("Register")
            username = st.sidebar.text_input("Enter a Username")
            password = st.sidebar.text_input("Enter a Password", type="password")
            confirm_password = st.sidebar.text_input("Confirm Password", type="password")
            if st.sidebar.button("Register"):
                if username in users:
                    st.sidebar.error("User already exists.")
                elif password != confirm_password:
                    st.sidebar.error("Passwords do not match.")
                else:
                    users[username] = password
                    st.sidebar.success("Registration successful. Please log in.")
        
        if action == "Login":
            st.sidebar.header("Login")
            username = st.sidebar.text_input("Username")
            password = st.sidebar.text_input("Password", type="password")
            if st.sidebar.button("Login"):
                if username in users and users[username] == password:
                    st.session_state['authenticated'] = True
                    st.sidebar.success("Logged in successfully!")
                else:
                    st.sidebar.error("Invalid credentials.")
    else:
        # Welcome Page
        st.image("avocado_image.jpg", use_column_width=True)
        st.header("Welcome to Avocado Price Prediction!")
        
        # Exploratory Data Analysis (EDA)
        st.subheader("Exploratory Data Analysis (EDA)")
        st.write("Here are some insights from the dataset:")
        st.write("Top 5 rows of the dataset:")
        st.dataframe(avocado_data.head())
        st.write("Summary Statistics:")
        st.write(avocado_data.describe())
        st.write("Missing values in the dataset:")
        st.write(avocado_data.isnull().sum())

        # Prediction Page
        st.subheader("Predict Avocado Prices")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            total_volume = st.number_input("Total Volume")
        with col2:
            plu4046 = st.number_input("PLU 4046")
        with col3:
            plu4225 = st.number_input("PLU 4225")
        with col4:
            plu4770 = st.number_input("PLU 4770")
        with col5:
            total_bags = st.number_input("Total Bags")
        
        type_option = st.selectbox("Select Type", avocado_data['type'].unique())
        region_option = st.selectbox("Select Region", avocado_data['region'].unique())
        
        if st.button("Predict"):
            input_data = pd.DataFrame({
                'TotalVolume': [total_volume],
                'plu4046': [plu4046],
                'plu4225': [plu4225],
                'plu4770': [plu4770],
                'TotalBags': [total_bags],
                'SmallBags': [0],  # Default or calculate based on logic
                'LargeBags': [0],  # Default or calculate based on logic
                'XLargeBags': [0],  # Default or calculate based on logic
                'type': [type_option],
                'region': [region_option]
            })
            transformed_input = preprocessor.transform(input_data)
            prediction = random_forest_model.predict(transformed_input)
            st.success(f"Predicted Average Price: ${prediction[0]:.2f}")
        
        # Contact Information
        st.subheader("Contact Us")
        st.text("Email: support@avocadoapp.com")
        st.text("Phone: +1-800-AVOCADO")
        st.text("Address: 123 Avocado Lane, Fruitville, USA")

if __name__ == '__main__':
    main()
