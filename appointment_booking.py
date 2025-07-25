# appointment_booking.py
import streamlit as st
from datetime import datetime, time, date
from db_manager import DBManager # Import the new DBManager

class AppointmentBookingPage:
    """Handles the selection of hospital, department, doctor, date, and time for an appointment."""

    HOSPITAL_DATA = {
        "City Hospital": {
            "Cardiology": [
                {"name": "Dr. A. Sharma", "rating": 4.8, "qualification": "MD, DM (Cardiology)", "experience": "15 years"},
                {"name": "Dr. B. Verma", "rating": 4.6, "qualification": "MD, DNB (Cardiology)", "experience": "10 years"},
            ],
            "Neurology": [
                {"name": "Dr. C. Mehta", "rating": 4.7, "qualification": "MD, DM (Neurology)", "experience": "12 years"},
                {"name": "Dr. D. Nair", "rating": 4.5, "qualification": "MD, DNB (Neurology)", "experience": "9 years"},
            ],
        },
        "Green Valley Clinic": {
            "Orthopedics": [
                {"name": "Dr. E. Singh", "rating": 4.9, "qualification": "MS (Ortho), DNB (Ortho)", "experience": "18 years"},
                {"name": "Dr. F. Gupta", "rating": 4.6, "qualification": "MS (Ortho)", "experience": "11 years"},
            ],
            "Dermatology": [
                {"name": "Dr. O. Roy", "rating": 4.8, "qualification": "MD (Dermatology)", "experience": "11 years"},
                {"name": "Dr. P. Shah", "rating": 4.5, "qualification": "DDVL, MD (Dermatology)", "experience": "7 years"},
            ],
        }
    }

    def __init__(self):
        self.db_manager = DBManager()

    def display(self):
        st.title("🗓️ Book Your Appointment")
        st.markdown("Welcome! Please choose your hospital, department, doctor, and appointment time.")

        username = st.session_state.get('current_user')
        if not username:
            st.warning("Please log in to book an appointment.")
            return

        # Hospital & Department Selection
        st.markdown("### 🏥 Select Hospital & Department")
        col1, col2 = st.columns(2)
        with col1:
            hospital_names = list(self.HOSPITAL_DATA.keys())
            selected_hospital = st.selectbox("🏥 Hospital", hospital_names, key="select_hospital_dept")
            st.session_state.selected_hospital = selected_hospital

        with col2:
            departments = list(self.HOSPITAL_DATA[selected_hospital].keys())
            selected_department = st.selectbox("🩺 Department", departments, key="select_department_dept")
            st.session_state.selected_department = selected_department

        # Doctor Selection
        st.markdown("### 👨‍⚕️ Choose a Doctor")
        doctors = self.HOSPITAL_DATA[selected_hospital][selected_department]
        doctor_labels = [
            f"{doc['name']} (⭐ {doc['rating']}) - {doc['qualification']} - {doc['experience']}"
            for doc in doctors
        ]
        selected_doctor_label = st.selectbox("👨‍⚕️ Doctor", doctor_labels, key="select_doctor_dept")
        doc_index = doctor_labels.index(selected_doctor_label)
        selected_doctor = doctors[doc_index]
        st.session_state.selected_doctor = selected_doctor

        # Doctor Info Card
        st.markdown(f"""
        **👨‍⚕️ Doctor Selected:** `{selected_doctor['name']}`
        **📚 Qualification:** `{selected_doctor['qualification']}`
        **🧠 Experience:** `{selected_doctor['experience']}`
        **⭐ Rating:** `{selected_doctor['rating']}`
        """)

        st.markdown("---")

        # Date and Time Picker
        st.markdown("### 📅 Select Date & Time TO 🕒 Book a Slot ")

        if "appointment_time" not in st.session_state:
            st.session_state.appointment_time = time(9, 0) # Default 9:00 AM

        appointment_date = st.date_input("📅 Appointment Date", datetime.today(), key="appointment_date_dept")
        time_value = st.session_state.appointment_time if isinstance(st.session_state.appointment_time, time) else time(9, 0)
        appointment_time = st.time_input("🕒 Appointment Time", value=time_value, key="appointment_time_dept")
        st.session_state.appointment_time = appointment_time
        st.session_state.appointment_date = appointment_date.strftime("%Y-%m-%d")

        st.markdown("---")

        # Save Button
        col_space1, col_button, col_space2 = st.columns([1, 2, 1])
        with col_button:
            if st.button("✅ Save Appointment Details", use_container_width=True, key="save_appointment_details_dept"):
                new_booked_appointment = {
                    "Hospital": selected_hospital,
                    "Department": selected_department,
                    "Doctor": selected_doctor['name'],
                    "Date": appointment_date.strftime("%Y-%m-%d"),
                    "Time": appointment_time.strftime("%H:%M:%S"), # Store as HH:MM:SS in DB
                    "booking_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                # Check if the appointment already exists
                exists = self.db_manager.appointment_exists(username, new_booked_appointment)

                if not exists:
                    success = self.db_manager.add_booked_appointment(username, new_booked_appointment)
                    if success is not None:
                        st.success("✅ Appointment details saved successfully!")
                    else:
                        st.error("🔴 Failed to save appointment details. Please try again.")
                else:
                    st.info("ℹ️ This exact appointment is already saved.")