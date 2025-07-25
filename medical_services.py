# medical_services.py
import streamlit as st
from datetime import datetime, timedelta
from db_manager import DBManager # Import the new DBManager

class MedicalServicesPage:
    """Provides details on hospital fees, allows health data input, slot booking, and shows nearby medical shops."""

    HOSPITALS = {
        "City Hospital": {
            "Cardiology": {"Consultation": "₹500", "ECG": "₹1200"},
            "Neurology": {"Consultation": "₹600", "MRI": "₹3000"},
            "Pediatrics": {"Consultation": "₹400"}
        },
        "Green Valley Clinic": {
            "Orthopedics": {"Consultation": "₹450", "X-Ray": "₹800"},
            "Dermatology": {"Consultation": "₹350"},
            "Radiology": {"CT Scan": "₹2500"}
        },
        "Sunrise Medical Center": {
            "Oncology": {"Consultation": "₹700", "Chemotherapy": "₹5000"},
            "Emergency": {"Emergency Care": "₹1000"},
            "Radiology": {"MRI": "₹3200"}
        }
    }

    MEDICAL_SHOPS = {
        "HealthPlus Pharmacy": 2.1,
        "CityCare Medicals": 3.5,
        "Wellness Drugstore": 1.8,
        "MediQuick": 4.0
    }

    def __init__(self):
        self.db_manager = DBManager()

    @staticmethod
    def _generate_slots():
        slots = []
        today = datetime.today()
        for i in range(7):
            day = today + timedelta(days=i)
            date_str = day.strftime("%Y-%m-%d")
            slots.append({"date": date_str, "times": ["09:00 AM", "01:00 PM", "05:00 PM"]})
        return slots

    def display(self):
        st.title("Hospital and Department Fee Structure")

        username = st.session_state.get('current_user')
        if not username:
            st.warning("Please log in to view medical services.")
            return

        # Hospital dropdown
        selected_hospital = st.selectbox("Select Hospital", list(self.HOSPITALS.keys()))

        if selected_hospital:
            st.subheader(f"Departments in {selected_hospital}")
            departments = self.HOSPITALS[selected_hospital]
            for dept, fees in departments.items():
                st.markdown(f"### {dept}")
                for service, cost in fees.items():
                    st.write(f"- {service}: {cost}")

        st.markdown("---")
   

        # Nearby medical shops dropdown
        st.subheader("Nearby Medical Shops")
        shop_names = list(self.MEDICAL_SHOPS.keys())
        selected_shop = st.selectbox("Select Medical Shop", shop_names)

        if selected_shop:
            dist = self.MEDICAL_SHOPS[selected_shop]
            st.write(f"Distance of **{selected_shop}** from hospital: {dist} km")

        st.markdown("---")

        # Show Recorded Data & Print Button
        show_data = st.button("Show Recorded Data & Print", type="primary")

        if show_data:
            st.header("Recorded Data Summary")
            st.subheader("Selected Hospital & Departments Fees")
            st.write(f"**Hospital:** {selected_hospital}")
            for dept, fees in self.HOSPITALS[selected_hospital].items():
                st.write(f"**{dept}**")
                for service, cost in fees.items():
                    st.write(f"- {service}: {cost}")
                    
            st.subheader("Selected Medical Shop")
            st.write(f"**{selected_shop}** — {self.MEDICAL_SHOPS[selected_shop]} km from hospital")

            # Print button (opens browser print dialog)
            st.markdown(
                """
                <br>
                <button onclick="window.print()" style="background-color:#4e8cff;color:white;padding:10px 20px;border:none;border-radius:5px;font-size:1rem;cursor:pointer;">
                    🖨️ Print This Page
                </button>
                """,
                unsafe_allow_html=True
            )
