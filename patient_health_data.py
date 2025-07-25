# patient_health_data.py
import streamlit as st
from datetime import datetime
from db_manager import DBManager # Import the new DBManager

class PatientHealthDataPage:
    """Manages the patient health data entry and display."""

    def __init__(self):
        self.db_manager = DBManager()

    def display(self):
        st.title("📝 Patient Health Data Entry")
        st.markdown("Please provide your health details below to help us serve you better. 🩺")

        username = st.session_state.get('current_user')
        if not username:
            st.warning("Please log in to enter health data.")
            return

        health_data = self.db_manager.get_last_health_data(username)
        if not health_data: # If no data exists, set defaults
            health_data = {}

        with st.form(key='health_data_form'):
            st.subheader("Your Vital Information")
            weight = st.number_input("⚖️ Weight (kg)", min_value=0.0, value=float(health_data.get("weight", 70.0)), step=0.1)
            height = st.number_input("📏 Height (cm)", min_value=0.0, value=float(health_data.get("height", 170.0)), step=0.1)
            bp = st.text_input("🩸 Blood Pressure (mmHg)", value=health_data.get("bp", "120/80"), placeholder="e.g., 120/80")
            
            st.subheader("Your Symptoms & Medical History")
            symptoms = st.text_area("🤒 Symptoms (e.g., fever, headache, cough)", value=health_data.get("symptoms", ""), height=100)
            pre_meds = st.text_area("💊 Pre-existing Conditions / Current Medications (if any)", value=health_data.get("pre_meds", ""), height=100)

            submit_button = st.form_submit_button("💾 Save Health Data")

            if submit_button:
                current_record = {
                    "weight": weight,
                    "height": height,
                    "symptoms": symptoms,
                    "pre_meds": pre_meds,
                    "bp": bp,
                    "record_date": datetime.today().strftime("%Y-%m-%d")
                }
                success = self.db_manager.save_health_data(username, current_record)
                if success is not None:
                    st.success("🟢 Health data saved successfully! 🎉")
                    st.rerun() # Rerun to update displayed data immediately
                else:
                    st.error("🔴 Failed to save health data. Please try again.")


        st.markdown("---")
        st.subheader("Last Recorded Health Data:")
        updated_health_data = self.db_manager.get_last_health_data(username) # Fetch again to show latest
        if updated_health_data:
            st.info(f"""
            **🗓 Last Update:** {updated_health_data.get('record_date', 'N/A')}
            **⚖️ Weight:** {updated_health_data.get('weight', 'N/A')} kg
            **📏 Height:** {updated_health_data.get('height', 'N/A')} cm
            **🩸 Blood Pressure:** {updated_health_data.get('bp', 'N/A')}
            **🤒 Symptoms:** {updated_health_data.get('symptoms', 'N/A')}
            **💊 Pre-Medicine:** {updated_health_data.get('pre_meds', 'N/A')}
            """)
        else:
            st.write("No health data recorded yet.")