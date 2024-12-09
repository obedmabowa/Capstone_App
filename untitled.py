import streamlit as st
import bcrypt
import json
import os

# File to store user credentials
CREDENTIALS_FILE = "users.json"

# Helper functions
def load_credentials():
    """Load user credentials from a file."""
    if not os.path.exists(CREDENTIALS_FILE):
        return {}
    with open(CREDENTIALS_FILE, 'r') as file:
        return json.load(file)

def save_credentials(credentials):
    """Save user credentials to a file."""
    with open(CREDENTIALS_FILE, 'w') as file:
        json.dump(credentials, file)

def hash_password(password):
    """Hash a password for secure storage."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(password, hashed):
    """Verify a password against a stored hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

# Load existing credentials
credentials = load_credentials()

# Sidebar for authentication
auth_option = st.sidebar.radio("Choose Option", ["Log In", "Sign Up"])

if auth_option == "Sign Up":
    st.title("Sign Up")
    new_username = st.text_input("Choose a Username")
    new_password = st.text_input("Choose a Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):
        if new_password != confirm_password:
            st.error("Passwords do not match!")
        elif new_username in credentials:
            st.error("Username already exists!")
        else:
            # Save the new user
            credentials[new_username] = hash_password(new_password).decode('utf-8')
            save_credentials(credentials)
            st.success("User registered successfully! Please log in.")
elif auth_option == "Log In":
    st.title("Log In")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Log In"):
        if username in credentials and verify_password(password, credentials[username].encode('utf-8')):
            st.success(f"Welcome, {username}!")
            # Display the app options (EDA and prediction) only for logged-in users
            options = st.radio("Choose an Option", ["Predict Price", "EDA"])

            # Predict Price Section
            if options == "Predict Price":
                st.write("Price Prediction Section")
                # Add your price prediction code here (e.g., input fields and predictions)
            
            # EDA Section
            elif options == "EDA":
                st.write("Exploratory Data Analysis Section")
                # Add your EDA code here
        else:
            st.error("Invalid username or password!")
