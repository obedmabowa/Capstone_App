import streamlit as st
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor

# Load the trained model
model = joblib.load('random_forest_model.pkl')

# Define the preprocessor (assuming you used a similar preprocessor in training)
categorical_features = ['type', 'region']
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ],
    remainder='passthrough'
)

# Create a pipeline with the preprocessor and model
pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('model', model)])

# Streamlit app
st.title("Avocado Price Prediction")

# Input widgets for the features
date = st.date_input("Date")
average_price = st.number_input("Average Price", min_value=0.0, step=0.01)
total_volume = st.number_input("Total Volume", min_value=0.0, step=0.01)
plu4046 = st.number_input("PLU4046", min_value=0.0, step=0.01)
plu4225 = st.number_input("PLU4225", min_value=0.0, step=0.01)
plu4770 = st.number_input("PLU4770", min_value=0.0, step=0.01)
total_bags = st.number_input("Total Bags", min_value=0.0, step=0.01)
small_bags = st.number_input("Small Bags", min_value=0.0, step=0.01)
large_bags = st.number_input("Large Bags", min_value=0.0, step=0.01)
xlarge_bags = st.number_input("XLarge Bags", min_value=0.0, step=0.01)
type_ = st.selectbox("Type", ['conventional', 'organic'])
region = st.selectbox("Region", ['Albany', 'Atlanta', 'BaltimoreWashington'])

# Prepare data for prediction
input_data = pd.DataFrame({
    'Date': [pd.to_datetime(date)],
    'AveragePrice': [average_price],
    'TotalVolume': [total_volume],
    'plu4046': [plu4046],
    'plu4225': [plu4225],
    'plu4770': [plu4770],
    'TotalBags': [total_bags],
    'SmallBags': [small_bags],
    'LargeBags': [large_bags],
    'XLargeBags': [xlarge_bags],
    'type': [type_],
    'region': [region]
})

# Make prediction
if st.button("Predict"):
    prediction = pipeline.predict(input_data.drop(columns='Date'))
    st.write(f"Predicted Avocado Price: ${prediction[0]:.2f}")