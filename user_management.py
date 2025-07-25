# user_management.py
import os
import re
import random
import string
import base64
import streamlit as st
import pandas as pd
from db_manager import DBManager # Import the new DBManager

USER_DATA_FILE = "user_data.json" # Kept for consistency but not used for data storage anymore

class UserManager:
    """Manages user authentication, registration, and related utilities."""

    INDIAN_STATES_CITIES = {
        "Andhra Pradesh": ["Visakhapatnam", "Vijayawada", "Guntur"],
        "Arunachal Pradesh": ["Itanagar", "Tawang", "Pasighat"],
        "Assam": ["Guwahati", "Silchar", "Dibrugarh"],
        "Bihar": ["Patna", "Gaya", "Bhagalpur"],
        "Chhattisgarh": ["Raipur", "Bhilai", "Bilaspur"],
        "Goa": ["Panaji", "Margao", "Vasco da Gama"],
        "Gujarat": ["Ahmedabad", "Surat", "Vadodara"],
        "Haryana": ["Gurgaon", "Faridabad", "Panipat"],
        "Himachal Pradesh": ["Shimla", "Manali", "Dharamshala"],
        "Jharkhand": ["Ranchi", "Jamshedpur", "Dhanbad"],
        "Karnataka": ["Bengaluru", "Mysuru", "Mangalore"],
        "Kerala": ["Thiruvananthapuram", "Kochi", "Kozhikode"],
        "Madhya Pradesh": ["Bhopal", "Indore", "Gwalior"],
        "Maharashtra": ["Mumbai", "Pune", "Nagpur"],
        "Manipur": ["Imphal", "Thoubal", "Bishnupur"],
        "Meghalaya": ["Shillong", "Tura", "Jowai"],
        "Mizoram": ["Aizawl", "Lunglei", "Champhai"],
        "Nagaland": ["Kohima", "Dimapur", "Mokokchung"],
        "Odisha": ["Bhubaneswar", "Cuttack", "Rourkela"],
        "Punjab": ["Ludhiana", "Amritsar", "Jalandhar"],
        "Rajasthan": ["Jaipur", "Jodhpur", "Udaipur"],
        "Sikkim": ["Gangtok", "Namchi", "Geyzing"],
        "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai"],
        "Telangana": ["Hyderabad", "Warangal", "Nizamabad"],
        "Tripura": ["Agartala", "Udaipur", "Dharmanagar"],
        "Uttar Pradesh": ["Lucknow", "Kanpur", "Varanasi"],
        "Uttarakhand": ["Dehradun", "Haridwar", "Nainital"],
        "West Bengal": ["Kolkata", "Howrah", "Durgapur"],
        "Delhi": ["New Delhi", "Dwarka", "Rohini"],
        "Jammu and Kashmir": ["Srinagar", "Jammu", "Anantnag"],
        "Ladakh": ["Leh", "Kargil"]
    }

    def __init__(self):
        self.db_manager = DBManager()

    def load_users(self):
        return self.db_manager.get_users()

    def save_user(self, user_data):
        return self.db_manager.add_user(user_data)

    def user_exists(self, username):
        return self.db_manager.user_exists(username)

    def check_credentials(self, username, password):
        return self.db_manager.check_credentials(username, password)

    @staticmethod
    def is_valid_username(username):
        return len(re.findall(r'[A-Za-z]', username)) >= 3

    @staticmethod
    def is_valid_password(password):
        has_upper = re.search(r'[A-Z]', password)
        has_digit = re.search(r'\d', password)
        has_special = re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
        return bool(has_upper and has_digit and has_special)

    @staticmethod
    def is_valid_email(email):
        pattern = r'^[\w\.-]+@gmail\.com$'
        return re.match(pattern, email) is not None

    @staticmethod
    def generate_captcha(length=5):
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choices(chars, k=length))

    @staticmethod
    def set_background(image_file):
        if not os.path.isfile(image_file):
            st.error(f"Background image '{image_file}' not found in {os.getcwd()}.")
            return
        ext = image_file.split('.')[-1]
        with open(image_file, "rb") as image:
            encoded = base64.b64encode(image.read()).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/{ext};base64,{encoded}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )