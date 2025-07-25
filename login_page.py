# pages/login_page.py
import streamlit as st
from user_management import UserManager

class LoginPage:
    """Represents the login page for existing users."""

    def __init__(self, user_manager: UserManager):
        self.user_manager = user_manager

    def display(self):
        st.title("Existing User Login 🔐")

        username = st.text_input("Username", placeholder="e.g., john_doe", help="At least 3 letters")
        password = st.text_input("Password", type="password", placeholder="Strong password (min 8 chars)", help="At least 1 uppercase, 1 number & 1 special char")

        # CAPTCHA
        st.markdown("---")
        if "captcha" not in st.session_state:
            st.session_state.captcha = self.user_manager.generate_captcha()

        col1, col2 = st.columns([0.6, 0.4])
        with col1:
            st.markdown(f"<h3 style='color:#004b8d;'>CAPTCHA: <span style='background-color:#f0f0f0; padding: 5px 10px; border-radius: 5px; font-family: monospace; letter-spacing: 2px;'>{st.session_state.captcha}</span></h3>", unsafe_allow_html=True)
        with col2:
            if st.button("🔄 Refresh Captcha"):
                st.session_state.captcha = self.user_manager.generate_captcha()
                st.rerun()

        captcha_input = st.text_input("Enter the CAPTCHA above ⬆️")
        st.markdown("---")

        if st.button("Login ➡️"):
            if not self.user_manager.is_valid_username(username):
                st.error("Username must contain at least 3 letters (A-Z or a-z). 😔")
            elif not self.user_manager.is_valid_password(password):
                st.error("Password must contain at least one uppercase letter, one number, and one special character. 🔑")
            elif not self.user_manager.user_exists(username):
                st.error("User does not exist. Please register first. 🙅‍♀️")
            elif not self.user_manager.check_credentials(username, password):
                st.error("Incorrect password. Please try again. 🚫")
            elif captcha_input.strip().upper() != st.session_state.captcha:
                st.error("Incorrect captcha. Please try again. 🤖")
                st.session_state.captcha = self.user_manager.generate_captcha() # Refresh captcha on failure
                st.rerun()
            else:
                st.session_state.logged_in = True
                st.session_state.current_user = username
                st.success("Login successful! Welcome! 🎉")
                if "captcha" in st.session_state: # Clear captcha after successful login
                    del st.session_state.captcha
                st.rerun()

        # Custom CSS for better input fields and buttons
        st.markdown("""
            <style>
            .stTextInput > div > div > input {
                border-radius: 8px;
                border: 1px solid #ccc;
                padding: 10px;
            }
            .stButton > button {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border-radius: 8px;
                border: none;
                font-size: 16px;
                cursor: pointer;
                transition: background-color 0.3s;
            }
            .stButton > button:hover {
                background-color: #45a049;
            }
            </style>
        """, unsafe_allow_html=True)