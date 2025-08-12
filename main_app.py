import streamlit as st
import requests
import base64
from user_management import UserManager
from patient_health_data import PatientHealthDataPage
from appointment_booking import AppointmentBookingPage
from appointment_summary import AppointmentSummaryPage
from medical_services import MedicalServicesPage
from login_page import LoginPage
from register_page import RegistrationPage
from db_manager import DBManager
from landing import LandingPage


class MainApplication:
    """
    Manages the overall Streamlit application flow, user authentication,
    and navigation between different pages.
    """

    def __init__(self):
        self.db_manager = DBManager()
        self.user_manager = UserManager()
        self.login_page = LoginPage(self.user_manager)
        self.register_page = RegistrationPage(self.user_manager)
        self.landing = LandingPage()
        self.appointment_booking_page = AppointmentBookingPage()
        self.appointment_summary_page = AppointmentSummaryPage()
        self.patient_health_data_page = PatientHealthDataPage()
        self.medical_services_page = MedicalServicesPage()

    def set_background(self):
        """
        Always use GitHub raw image for Streamlit Cloud compatibility.
        """
        github_url = "https://github.com/vaibhav21493/queuemanagement/blob/main/quemain.png?raw=true"
        try:
            response = requests.get(github_url)
            if response.status_code == 200:
                encoded_img = base64.b64encode(response.content).decode()
                st.markdown(
                    f"""
                    <style>
                    .stApp {{
                        background-image: url("data:image/png;base64,{encoded_img}");
                        background-size: cover;
                        background-repeat: no-repeat;
                        background-attachment: fixed;
                        background-position: center;
                    }}
                    </style>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.error(f"Failed to load background image. HTTP {response.status_code}")
        except Exception as e:
            st.error(f"Error loading background: {e}")

    def run(self):
        # ✅ Set background globally
        self.set_background()

        # Initialize session state
        st.session_state.setdefault("page", "landing")
        st.session_state.setdefault("logged_in", False)
        st.session_state.setdefault("current_user", "")

        # Before login
        if not st.session_state.logged_in:
            if st.session_state.page == "landing":
                self.landing.display()
                return
            if st.session_state.page == "auth":
                page_choice = st.sidebar.radio("Choose Action", ["Login", "Register"])
                if page_choice == "Login":
                    self.login_page.display()
                elif page_choice == "Register":
                    self.register_page.display()
                return

        # Logged-in view
        if st.session_state.logged_in:
            st.sidebar.markdown(f"**Welcome, `{st.session_state.current_user}`! 🎉**")
            st.sidebar.markdown("---")

            page_choice = st.sidebar.radio(
                "Navigation",
                ["Departments", "Book Appointment", "Patient Health Data", "Medical Services"],
                key="logged_in_nav"
            )

            if page_choice == "Departments":
                self.appointment_booking_page.display()
            elif page_choice == "Book Appointment":
                self.appointment_summary_page.display()
            elif page_choice == "Patient Health Data":
                self.patient_health_data_page.display()
            elif page_choice == "Medical Services":
                self.medical_services_page.display()

            st.sidebar.markdown("---")
            if st.sidebar.button("🚪 Logout"):
                self.logout()

        self.apply_sidebar_style()

    def apply_sidebar_style(self):
        st.markdown("""
            <style>
            [data-testid="stSidebar"] {
                background: #e0f2f1;
                color: #222;
            }
            [data-testid="stSidebar"] label {
                color: #00695c;
                font-weight: bold;
            }
            </style>
        """, unsafe_allow_html=True)

    def logout(self):
        keys_to_clear = [
            "logged_in", "current_user", "page",
            "selected_hospital", "selected_department", "selected_doctor",
            "appointment_date", "appointment_time",
        ]
        for key in keys_to_clear:
            st.session_state.pop(key, None)
        st.rerun()
