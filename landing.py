import streamlit as st
import base64
import os


def set_background(local_file=None, remote_url=None):
    """
    Set a background image from either a local file or an online URL.
    - local_file: Path to local image file
    - remote_url: Direct raw URL to the image (GitHub raw link, etc.)
    """
    if local_file and os.path.exists(local_file):
        # Load local image as base64
        with open(local_file, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
        ext = local_file.split('.')[-1].lower()
        mime = "png" if ext == "png" else "jpeg"
        background = f"data:image/{mime};base64,{encoded}"
    elif remote_url:
        # Use remote image link directly
        background = remote_url
    else:
        st.error("No valid background image found.")
        return

    # Apply background with CSS
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url('{background}');
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# ✅ Landing Page Class
class LandingPage:
    def display(self):
        # For cloud deployment, use GitHub raw link
        set_background(remote_url="https://raw.githubusercontent.com/vaibhav21493/queuemanagement/main/quemain.png")

        st.markdown("""
            <style>
            .info-card {
                background: rgba(255,255,255,0.95);
                border-radius: 18px;
                box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.13);
                padding: 24px 20px;
                max-width: 280px;
                min-height: 220px;
                text-align: center;
                margin-bottom: 12px;
                transition: box-shadow 0.2s;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
            }
            .info-card:hover {
                box-shadow: 0 12px 36px 0 rgba(31, 38, 135, 0.18);
            }
            .hospital-logo-img {
                width: 90px;
                height: 90px;
                object-fit: contain;
                border-radius: 16px;
                background: #fff;
                box-shadow: 0 2px 8px rgba(0,0,0,0.10);
                padding: 8px;
                margin-bottom: 10px;
            }
            .start-btn {
                background: linear-gradient(90deg,#4e8cff,#38d39f);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 16px 48px;
                font-size: 1.3rem;
                font-weight: bold;
                margin-top: 32px;
                box-shadow: 0 2px 12px rgba(0,0,0,0.13);
                cursor: pointer;
                transition: background 0.2s;
                text-align: center;
            }
            .start-btn:hover {
                background: linear-gradient(90deg,#38d39f,#4e8cff);
            }
            .logo-row {
                display: flex;
                justify-content: center;
                gap: 48px;
                margin-top: 20px;
                margin-bottom: 40px;
            }
            </style>
        """, unsafe_allow_html=True)

        # Welcome Text
        st.markdown("""
            <div style="display:flex; flex-direction: column; align-items: center; margin-top: 40px;">
                <h1 style="color: #22223b; margin-bottom: 12px; text-shadow: 2px 2px 8px #fff;">
                    👋 Welcome to <span style="color:#4e8cff;">Queue Management System</span>
                </h1>
                <p style="color:#22223b; font-size:1.1rem; margin-bottom: 0;">
                    Efficiently manage patient queues, reduce wait times, and enhance hospital experiences.<br>
                    <b>Explore our features below!</b>
                </p>
            </div>
        """, unsafe_allow_html=True)

        # Hospital Logos
        st.markdown("""
            <div class="logo-row">
                <img src="https://cdn-icons-png.flaticon.com/512/2965/2965567.png" class="hospital-logo-img">
                <img src="https://cdn-icons-png.flaticon.com/512/2965/2965568.png" class="hospital-logo-img">
                <img src="https://cdn-icons-png.flaticon.com/512/2965/2965569.png" class="hospital-logo-img">
            </div>
        """, unsafe_allow_html=True)

        # Info Cards
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
                <div class="info-card">
                    <h3>⏳ Live Queue Tracking</h3>
                    <p>Monitor real-time patient flow and waiting times for every department.</p>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
                <div class="info-card">
                    <h3>📱 Online Appointment Booking</h3>
                    <p>Book, reschedule, or cancel appointments online, reducing overcrowding.</p>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
                <div class="info-card">
                    <h3>📊 Analytics Dashboard</h3>
                    <p>Gain insights into patient volumes, peak hours, and bottlenecks.</p>
                </div>
            """, unsafe_allow_html=True)

        # Start Button
        st.markdown("<div style='display:flex; justify-content:center;'>", unsafe_allow_html=True)
        if st.button("Start 🚀", key="start_btn"):
            st.session_state.page = "auth"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


# ✅ Optional direct execution
if __name__ == "__main__":
    LandingPage().display()
