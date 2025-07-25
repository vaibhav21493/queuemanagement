# pages/register_page.py
import streamlit as st
from datetime import datetime
from user_management import UserManager

class RegistrationPage:
    """Represents the registration page for new users."""

    def __init__(self, user_manager: UserManager):
        self.user_manager = user_manager

    def display(self):
        st.title("New User Registration 📝")

        new_username = st.text_input("New Username", placeholder="e.g., jane_doe", help="Must contain at least 3 letters")
        new_password = st.text_input("New Password", type="password", placeholder="e.g., MySecureP@ss1", help="At least 1 uppercase, 1 number & 1 special char")
        full_name = st.text_input("Full Name", placeholder="e.g., Jane Elizabeth Doe")
        father_name = st.text_input("Father's Name", placeholder="e.g., Robert Doe")
        dob = st.date_input("Date of Birth", max_value=datetime.today(), help="Select your date of birth")
        email = st.text_input("Email (must end with @gmail.com)", placeholder="e.g., yourname@gmail.com")

        state = st.selectbox("State", sorted(self.user_manager.INDIAN_STATES_CITIES.keys()), help="Select your Indian state")
        city = st.selectbox("City", self.user_manager.INDIAN_STATES_CITIES[state], help="Select your city based on the state")
        country = st.selectbox("Country", ["India"], help="Your country of residence")

        if st.button("Register Account ✨"):
            if not self.user_manager.is_valid_username(new_username):
                st.error("Username must contain at least 3 letters (A-Z or a-z). 🤔")
            elif not self.user_manager.is_valid_password(new_password):
                st.error("Password must contain at least one uppercase letter, one number, and one special character. 🔒")
            elif not self.user_manager.is_valid_email(email):
                st.error("Email must be a valid Gmail address ending with '@gmail.com'. 📧")
            elif self.user_manager.user_exists(new_username):
                st.error("Username already exists. Please choose a different one. ❌")
            else:
                user_data = {
                    "username": new_username,
                    "password": new_password, # In a real app, hash this password!
                    "full_name": full_name,
                    "father_name": father_name,
                    "dob": dob.strftime("%Y-%m-%d"),
                    "email": email,
                    "city": city,
                    "state": state,
                    "country": country
                }
                self.user_manager.save_user(user_data)
                st.success("Registration successful! Please proceed to login. ✅")
                # Optional: Redirect to login page
                # st.session_state.page = "main" # This needs to be handled by MainApplication
                # st.rerun()

        # Custom CSS for input fields and buttons
        st.markdown("""
            <style>
            .stTextInput > div > div > input, .stDateInput > div > div > input, .stSelectbox > div > div > div > div {
                border-radius: 8px;
                border: 1px solid #ccc;
                padding: 10px;
            }
            .stButton > button {
                background-color: #2196F3;
                color: white;
                padding: 10px 20px;
                border-radius: 8px;
                border: none;
                font-size: 16px;
                cursor: pointer;
                transition: background-color 0.3s;
            }
            .stButton > button:hover {
                background-color: #1976D2;
            }
            </style>
        """, unsafe_allow_html=True)