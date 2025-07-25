# appointment_summary.py
import streamlit as st
import pandas as pd
from datetime import datetime
from db_manager import DBManager # Import the new DBManager

class AppointmentSummaryPage:
    """Displays the appointment summary and handles the payment process."""

    def __init__(self):
        self.db_manager = DBManager()

    def display(self):
        st.title("📃 Your Appointment Summary & Payment")

        username = st.session_state.get('current_user')
        if not username:
            st.warning("Please log in to view appointment summary.")
            return

        booked_appointments = self.db_manager.get_booked_appointments(username)

        # Retrieve current appointment details from session state
        selected_hospital = st.session_state.get('selected_hospital', "Not selected")
        selected_department = st.session_state.get('selected_department', "Not selected")
        selected_doctor_info = st.session_state.get('selected_doctor', {})
        appointment_date = st.session_state.get('appointment_date', datetime.today().strftime("%Y-%m-%d"))
        appointment_time = st.session_state.get('appointment_time', "09:00 AM")

        # Ensure date and time are in string format for display
        if isinstance(appointment_date, datetime):
            appointment_date = appointment_date.strftime("%Y-%m-%d")
        if not isinstance(appointment_time, str):
            appointment_time = str(appointment_time) # Convert time object to string

        doctor_name = selected_doctor_info.get('name', "Not selected") # Default if not found
        doctor_qualification = selected_doctor_info.get('qualification', 'N/A')
        doctor_experience = selected_doctor_info.get('experience', 'N/A')
        doctor_rating = selected_doctor_info.get('rating', 'N/A')

        health_data = self.db_manager.get_last_health_data(username)
        if not health_data:
            health_data = {}

        # CSS for blurred containers
        st.markdown("""
        <style>
        .blurred-container {
            background: rgba(255, 255, 255, 0.4);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-radius: 20px;
            padding: 28px;
            margin: 24px auto;
            max-width: 900px;
            box-shadow: 0 8px 30px rgba(31, 38, 135, 0.25);
            border: 1px solid rgba(255,255,255,0.3);
            color: #222;
        }
        .section h3 {
            color: #004b8d;
            border-bottom: 2px solid #4e8cff;
            padding-bottom: 8px;
            margin-bottom: 15px;
            font-size: 1.3rem;
        }
        ul {
            padding-left: 18px;
        }
        ul li {
            margin-bottom: 8px;
            font-size: 15px;
            line-height: 1.5;
        }
        </style>
        """, unsafe_allow_html=True)

        # Appointment Details container
        appointment_html = f"""
        <div class="blurred-container">
            <h3>🗓️ Appointment Details</h3>
            <ul>
                <li><b>🏥 Hospital:</b> {selected_hospital}</li>
                <li><b>🩺 Department:</b> {selected_department}</li>
                <li><b>👨‍⚕️ Doctor:</b> {doctor_name}</li>
                <li><b>📚 Qualification:</b> {doctor_qualification}</li>
                <li><b>🧠 Experience:</b> {doctor_experience}</li>
                <li><b>⭐ Rating:</b> {doctor_rating}</li>
                <li><b>📆 Date:</b> {appointment_date}</li>
                <li><b>⏰ Time:</b> {appointment_time}</li>
            </ul>
        </div>
        """
        st.markdown(appointment_html, unsafe_allow_html=True)

        # Patient Health Data container
        if health_data:
            patient_html = f"""
            <div class="blurred-container">
                <h3>🧾 Patient Health Data</h3>
                <ul>
                    <li><b>🗓 Record Date:</b> {health_data.get('record_date', 'N/A')}</li>
                    <li><b>⚖️ Weight:</b> {health_data.get('weight', 'N/A')} kg</li>
                    <li><b>📏 Height:</b> {health_data.get('height', 'N/A')} cm</li>
                    <li><b>🩸 Blood Pressure:</b> {health_data.get('bp', 'N/A')}</li>
                    <li><b>🤒 Symptoms:</b> {health_data.get('symptoms', 'N/A')}</li>
                    <li><b>💊 Pre-Medicine:</b> {health_data.get('pre_meds', 'N/A')}</li>
                </ul>
            </div>
            """
        else:
            patient_html = """
            <div class="blurred-container">
                <h3>🧾 Patient Health Data</h3>
                <p>No health data found. Please enter your details on the 'Patient Health Data' page.</p>
            </div>
            """
        st.markdown(patient_html, unsafe_allow_html=True)

        # Show all appointments in a table
        st.markdown("### 📝 All Booked Appointments")
        if booked_appointments:
            # Convert list of dictionaries to DataFrame for display
            df_appointments = pd.DataFrame(booked_appointments)
            st.dataframe(df_appointments, use_container_width=True)
        else:
            st.info("No appointments booked yet.")

        # Find your appointment number in the list (based on currently selected/saved in session)
        your_index = None
        current_appointment_details = {
            "Hospital": selected_hospital,
            "Department": selected_department,
            "Doctor": doctor_name,
            "Date": appointment_date,
            "Time": appointment_time # This needs to match the format from DB
        }

        for idx, appt in enumerate(booked_appointments):
            # Convert DB time format (HH:MM:SS) to AM/PM for comparison if needed
            db_time_am_pm = datetime.strptime(str(appt.get("appointment_time")), "%H:%M:%S").strftime("%I:%M %p") if isinstance(appt.get("appointment_time"), (str, type(None))) and appt.get("appointment_time") else appt.get("appointment_time")

            if (
                appt.get("hospital") == current_appointment_details["Hospital"] and
                appt.get("department") == current_appointment_details["Department"] and
                appt.get("doctor") == current_appointment_details["Doctor"] and
                str(appt.get("appointment_date")) == current_appointment_details["Date"] and
                db_time_am_pm == current_appointment_details["Time"]
            ):
                your_index = idx + 1
                break

        # Show your appointment number
        if your_index is not None:
            st.success(f"**Your Appointment Number is: {your_index}**")
        else:
            st.info("Your appointment details are not fully matched in the list.")


        st.markdown("---")
        st.header("Print and Payment")

        # Print button
        st.markdown("""
            <button onclick="window.print()" style="background-color:#007bff;color:white;padding:12px 28px;border:none;border-radius:8px;font-size:18px;cursor:pointer; transition: background-color 0.3s; margin-top: 20px; margin-bottom: 20px;">
                🖨️ Print Summary
            </button>
            """, unsafe_allow_html=True)

        payment_method = st.selectbox("💰 Select Payment Method", ["UPI", "Credit Card", "Debit Card", "Net Banking", "Cash"], key="payment_method_select")
        if st.button("💸 Pay Now", key="pay_now_button", help="Click to finalize your payment"):
            st.success(f"✅ Payment of your appointment via **{payment_method}** successful! Thank you for booking with us. Your appointment is confirmed.")