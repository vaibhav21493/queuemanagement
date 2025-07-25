# db_manager.py
import pymysql
import pandas as pd
from datetime import datetime, date, time
import sys # Import sys for printing errors to stderr

class DBManager:
    """Manages database connections and CRUD operations using pymysql."""

    def __init__(self, host='localhost', user='root', password='root', db='queue_management_db'):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.conn = None

    def connect(self):
        try:
            self.conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.db,
                cursorclass=pymysql.cursors.DictCursor # Returns dictionaries
            )
            # print("Connected to MySQL database!") # For debugging
        except pymysql.Error as e:
            # Error 1 & 2 Fix: Replaced st.error with print to sys.stderr
            print(f"Error connecting to MySQL: {e}", file=sys.stderr)
            self.conn = None
            raise # Re-raise the exception so the calling code can handle it

    def close(self):
        if self.conn and self.conn.open:
            self.conn.close()
            # print("MySQL connection closed.") # For debugging

    def _execute_query(self, query, params=None, fetch_one=False, fetch_all=False):
        # Attempt to connect/reconnect if connection is not open
        if not self.conn or not self.conn.open:
            try:
                self.connect()
            except pymysql.Error:
                # If connect fails, the exception is already printed/raised.
                # No need to print again here, just return None.
                return None

        if not self.conn: # If connection failed (e.g., due to previous `raise` in connect)
            return None

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, params)
                self.conn.commit()
                if fetch_one:
                    return cursor.fetchone()
                elif fetch_all:
                    return cursor.fetchall()
                return cursor.rowcount # For INSERT/UPDATE/DELETE
        except pymysql.Error as e:
            # Error 3 Fix: Replaced st.error with print to sys.stderr
            print(f"Database error during query execution: {e} | Query: {query} | Params: {params}", file=sys.stderr)
            self.conn.rollback() # Rollback changes on error
            return None
        finally:
            self.close() # Close connection after each operation for simplicity in Streamlit

    # --- User Management Operations ---
    def get_users(self):
        users_data = self._execute_query("SELECT * FROM users", fetch_all=True)
        if users_data:
            return pd.DataFrame(users_data)
        return pd.DataFrame() # Return empty DataFrame if no users

    def add_user(self, user_data):
        # Ensure dob is a date object for PyMySQL or string in 'YYYY-MM-DD'
        dob_date = user_data['dob']
        if isinstance(dob_date, str):
            dob_date = date.fromisoformat(dob_date) # Convert 'YYYY-MM-DD' string to date object

        query = """
        INSERT INTO users (username, password, full_name, father_name, dob, email, city, state, country)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            user_data['username'], user_data['password'], user_data['full_name'],
            user_data['father_name'], dob_date, user_data['email'],
            user_data['city'], user_data['state'], user_data['country']
        )
        return self._execute_query(query, params)

    def user_exists(self, username):
        query = "SELECT 1 FROM users WHERE username = %s"
        return bool(self._execute_query(query, (username,), fetch_one=True))

    def check_credentials(self, username, password):
        query = "SELECT 1 FROM users WHERE username = %s AND password = %s"
        return bool(self._execute_query(query, (username, password), fetch_one=True))

    # --- Health Data Operations (for PatientHealthDataPage) ---
    def save_health_data(self, username, health_data):
        # Ensure record_date is a date object
        record_date_obj = health_data['record_date']
        if isinstance(record_date_obj, str):
            record_date_obj = date.fromisoformat(record_date_obj)

        # Attempt to update if record for today exists, else insert
        query_check = "SELECT health_id FROM health_data WHERE username = %s AND record_date = %s"
        existing_record = self._execute_query(query_check, (username, record_date_obj), fetch_one=True)

        if existing_record:
            query = """
            UPDATE health_data SET weight = %s, height = %s, symptoms = %s, pre_meds = %s, bp = %s
            WHERE health_id = %s
            """
            params = (
                health_data['weight'], health_data['height'], health_data['symptoms'],
                health_data['pre_meds'], health_data['bp'], existing_record['health_id']
            )
        else:
            query = """
            INSERT INTO health_data (username, weight, height, symptoms, pre_meds, bp, record_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                username, health_data['weight'], health_data['height'], health_data['symptoms'],
                health_data['pre_meds'], health_data['bp'], record_date_obj
            )
        return self._execute_query(query, params)

    def get_last_health_data(self, username):
        query = "SELECT * FROM health_data WHERE username = %s ORDER BY record_date DESC LIMIT 1"
        return self._execute_query(query, (username,), fetch_one=True)

    # --- Appointment Operations ---
    def add_booked_appointment(self, username, appt_data):
        # Ensure date and time are appropriate objects
        appt_date_obj = appt_data['Date']
        if isinstance(appt_date_obj, str):
            appt_date_obj = date.fromisoformat(appt_date_obj)

        appt_time_obj = appt_data['Time']
        if isinstance(appt_time_obj, str):
            # Assuming "HH:MM:SS" format for database TIME column
            appt_time_obj = time.fromisoformat(appt_time_obj) 

        query = """
        INSERT INTO booked_appointments (username, hospital, department, doctor, appointment_date, appointment_time, booking_time)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            username, appt_data['Hospital'], appt_data['Department'], appt_data['Doctor'],
            appt_date_obj, appt_time_obj, appt_data['booking_time']
        )
        return self._execute_query(query, params)

    def get_booked_appointments(self, username):
        query = "SELECT * FROM booked_appointments WHERE username = %s ORDER BY appointment_date DESC, appointment_time DESC"
        appointments = self._execute_query(query, (username,), fetch_all=True)
        if appointments:
            # Convert datetime.time to string for consistent display
            for appt in appointments:
                if 'appointment_time' in appt and isinstance(appt['appointment_time'], time):
                    appt['appointment_time'] = appt['appointment_time'].strftime("%I:%M %p")
                # Convert datetime.date to string for consistent display
                if 'appointment_date' in appt and isinstance(appt['appointment_date'], date):
                    appt['appointment_date'] = appt['appointment_date'].strftime("%Y-%m-%d")
            return appointments
        return []

    def appointment_exists(self, username, appt_data):
        # Ensure date and time are appropriate objects for the query
        appt_date_obj = appt_data['Date']
        if isinstance(appt_date_obj, str):
            appt_date_obj = date.fromisoformat(appt_date_obj)

        appt_time_obj = appt_data['Time']
        if isinstance(appt_time_obj, str):
            # Assuming "HH:MM:SS" format for database TIME column
            appt_time_obj = time.fromisoformat(appt_time_obj)

        query = """
        SELECT 1 FROM booked_appointments
        WHERE username = %s AND hospital = %s AND department = %s AND doctor = %s
        AND appointment_date = %s AND appointment_time = %s
        """
        params = (
            username, appt_data['Hospital'], appt_data['Department'], appt_data['Doctor'],
            appt_date_obj, appt_time_obj
        )
        return bool(self._execute_query(query, params, fetch_one=True))


    # --- User Health History Operations (for MedicalServicesPage) ---
    def save_user_health_history(self, username, record_date, health_data):
        # Ensure record_date is a date object
        record_date_obj = record_date
        if isinstance(record_date_obj, str):
            record_date_obj = date.fromisoformat(record_date_obj)

        query_check = "SELECT history_id FROM user_health_history WHERE username = %s AND record_date = %s"
        existing_record = self._execute_query(query_check, (username, record_date_obj), fetch_one=True)

        if existing_record:
            query = """
            UPDATE user_health_history SET weight = %s, height = %s, bp = %s, sugar = %s
            WHERE history_id = %s
            """
            params = (
                health_data['weight'], health_data['height'], health_data['bp'], health_data['sugar'],
                existing_record['history_id']
            )
        else:
            query = """
            INSERT INTO user_health_history (username, record_date, weight, height, bp, sugar)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            params = (
                username, record_date_obj, health_data['weight'], health_data['height'],
                health_data['bp'], health_data['sugar']
            )
        return self._execute_query(query, params)

    def get_user_health_history(self, username):
        query = "SELECT * FROM user_health_history WHERE username = %s ORDER BY record_date DESC"
        history_data = self._execute_query(query, (username,), fetch_all=True)
        if history_data:
            # Convert list of dicts to a dict where keys are dates for easier access in page
            formatted_history = {}
            for item in history_data:
                # Convert datetime.date object to string for key consistency
                if 'record_date' in item and isinstance(item['record_date'], date):
                    item['record_date'] = item['record_date'].strftime("%Y-%m-%d")
                formatted_history[str(item['record_date'])] = item
            return formatted_history
        return {}
    
    